import streamlit as st
import tensorflow.compat.v1 as tf
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

st.set_page_config(layout="wide")
voc_file = "vocabulary_semantic.txt"

# Function to convert sparse tensor to strings
def sparse_tensor_to_strs(sparse_tensor):
    indices = sparse_tensor[0][0]
    values = sparse_tensor[0][1]
    dense_shape = sparse_tensor[0][2]
    strs = [[] for _ in range(dense_shape[0])]
    string = []
    ptr = 0
    b = 0

    for idx in range(len(indices)):
        if indices[idx][0] != b:
            strs[b] = string
            string = []
            b = indices[idx][0]

        string.append(values[ptr])

        ptr += 1

    strs[b] = string

    return strs

# Function to normalize the image
def normalize(image):
    return (255. - image) / 255.

# Function to resize the image
def resize(image, height):
    width = int(float(height * image.shape[1]) / image.shape[0])
    sample_img = cv2.resize(image, (width, height))
    return sample_img

@st.cache_resource
def load_model():

    # Define the paths and model information
    model = "Semantic-Model/semantic_model.meta"

    # Start a TensorFlow session
    sess = tf.compat.v1.InteractiveSession()
    tf.disable_eager_execution()

    # Restore the model and extract necessary tensors from the graph
    saver = tf.compat.v1.train.import_meta_graph(model)
    saver.restore(sess, model[:-5])
    graph = tf.compat.v1.get_default_graph()
    logits = tf.compat.v1.get_collection("logits")[0]

    return sess,graph,logits

def main():
    st.title("Music Sheet Transcriber")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    # Load TensorFlow model
    sess,graph,logits = load_model()

    input = graph.get_tensor_by_name("model_input:0")
    seq_len = graph.get_tensor_by_name("seq_lengths:0")
    rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
    height_tensor = graph.get_tensor_by_name("input_height:0")
    width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")

    # Extract necessary constants from the model
    WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

    decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert('L')
        img = np.array(img)

        img = resize(img, HEIGHT)
        img = normalize(img)
        img = np.expand_dims(img, axis=-1)  # Add a single channel dimension
        img = np.expand_dims(img, axis=0)  # Add a batch dimension

        dict_file = open(voc_file, 'r')
        dict_list = dict_file.read().splitlines()
        int2word = dict()
        for word in dict_list:
            word_idx = len(int2word)
            int2word[word_idx] = word
            dict_file.close()

        seq_lengths = [img.shape[2] / WIDTH_REDUCTION]
        prediction = sess.run(decoded, feed_dict={input: img, seq_len: seq_lengths, rnn_keep_prob: 1.0})
        str_predictions = sparse_tensor_to_strs(prediction)

        array_of_notes = []
        for w in str_predictions[0]:
            array_of_notes.append(int2word[w])
        notes = []
        for i in array_of_notes:
            if i[0:5] == "note-":
                if not i[6].isdigit():
                    notes.append(i[5:7])
                else:
                    notes.append(i[5])

        img = Image.open(uploaded_file).convert('L')
        size = (img.size[0], int(img.size[1]*1.5))


        layer = Image.new('RGB', size, (255, 255, 255))
        layer.paste(img, box=None)

        img_arr = np.array(layer)
        height = int(img_arr.shape[0])
        width = int(img_arr.shape[1])
        draw = ImageDraw.Draw(layer)
        font = ImageFont.truetype("Aaargh.ttf", 20)
        j = width / 9
        for i in notes:
            draw.text((j, height-40), i, (0, 0, 0), font=font)
            j += (width / (len(notes) + 4))
        st.image(layer)
    
        annotated_img_path = "annotated_image.png"  # Path to the annotated image
        layer.save(annotated_img_path)  # Save the annotated image

        with open(annotated_img_path, 'rb') as file:
                st.download_button(label='Download Annotated Image', data=file, file_name='annotated_image.png', mime='image/png')



if __name__ == "__main__":
    main()
