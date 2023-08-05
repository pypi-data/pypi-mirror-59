"""Queenbee Arguments class.

Arguments includes the input arguments to a task or a workflow.

Queenbee accepts two types of arguments:

    1. Parameters: A ``parameter`` is a variable that can be passed to a task or a
        workflow.
    2. Artifact: An ``artifact`` is a file or folder that can be identified by a url or
        a path.
"""
from queenbee.schema.qutil import BaseModel
from queenbee.schema.artifact_location import VerbEnum
from pydantic import Schema
from typing import List, Any, Optional, Dict


class Parameter(BaseModel):
    """Parameter.

    Parameter indicate a passed string parameter to a service template with an optional
    default value.
    """
    name: str = Schema(
        ...,
        description='Name is the parameter name. must be unique within a task\'s '
        'inputs / outputs.'
    )

    value: Any = Schema(
        None,
        description='Default value to use for an input parameter if a value was not'
        ' supplied.'
    )

    description: str = Schema(
        None,
        description='Optional description for input parameter.'
    )

    path: str = Schema(
        None,
        description='load parameters from a file. File can be a JSON / YAML or a text file.'
    )


class Artifact(BaseModel):
    """Artifact indicates an artifact to place at a specified path"""

    name: str = Schema(
        ...,
        description='name of the artifact. must be unique within a task\'s '
        'inputs / outputs.'
    )

    location: str = Schema(
        None,
        description="Name of the Artifact Location to source this artifact from."
    )

    source_path: str = Schema(
        None,
        description='Path to the artifact on the local machine, url or S3 bucket.'
    )

    path: str = Schema(
        None,
        description='Path the artifact should be copied to in the temporary task folder.'
    )

    description: str = Schema(
        None,
        description='Optional description for input parameter.'
    )

    headers: Optional[Dict[str, str]] = Schema(
        None,
        description="An object with Key Value pairs of HTTP headers. For artifacts from URL Location only"
    )

    verb: Optional[VerbEnum] = Schema(
        None,
        description="The HTTP verb to use when making the request. For artifacts from URL Location only"
    )


class Arguments(BaseModel):
    """Arguments to a task or a workflow.

    Queenbee accepts two types of arguments: parameters and artifacts. A ``parameter``
    is a variable that can be passed to a task or a workflow. An ``artifact`` is a file
    or folder that can be identified by a url or a path.
    """

    parameters: List[Parameter] = Schema(
        None,
        description='Parameters is the list of input parameters to pass to the task '
        'or workflow. A parameter can have a default value which will be overwritten if '
        'an input value is provided.'
    )

    artifacts: List[Artifact] = Schema(
        None,
        description='Artifacts is the list of file and folder arguments to pass to the '
        'task or workflow.'
    )
