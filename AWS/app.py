#!/usr/bin/env python3

from aws_cdk import core
from aws.ECS_Farget import ServerlessContainersArchitectureWithFargateStack


app = core.App()
ServerlessContainersArchitectureWithFargateStack(app, "icheckifyOcrMarker")

app.synth()
