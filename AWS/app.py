#!/usr/bin/env python3

import aws_cdk as core
from aws.ECS_Farget import ServerlessContainersArchitectureWithFargateStack


app = core.App()
ServerlessContainersArchitectureWithFargateStack(app, "icheckifyOcrMarker")

app.synth()
