#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import {OmrStack} from '../lib/omr-ecs-stack';

const app = new cdk.App();

const OmrEcsApp= new OmrStack(app, 'OmrStack', {

});