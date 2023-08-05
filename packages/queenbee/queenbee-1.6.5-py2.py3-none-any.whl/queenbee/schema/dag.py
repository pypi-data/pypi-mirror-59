"""Queenbee DAG steps.

A DAG step defines a single step in the workflow. Each step indicates what task should be
used and maps inputs and outputs for the specific task.
"""
from queenbee.schema.qutil import BaseModel
from queenbee.schema.arguments import Arguments
from pydantic import Schema
from typing import List, Any, Union


class LoopControl(BaseModel):
    """Control object for loops."""

    loop_var: str = Schema(
        'item',
        description='Name of variable which will be referenced in task.'
    )

    pause: int = Schema(
        None,
        description='Number of seconds to pause between the loops.'
    )

    # TODO: Add validator for this case.
    iterable_type: str = Schema(
        'list',
        description='Iterable object type: list | object'
    )

    parallel: bool = Schema(
        True,
        description='A switch to indicate if loops should be executed in serial or'
        ' parallel.'
    )


class DAGTask(BaseModel):
    """DAGTask defines a single step in a Directed Acyclic Graph (DAG) workflow."""

    name: str = Schema(
        ...,
        description='Name for this step. It must be unique in DAG.'
    )

    arguments: Arguments = Schema(
        None,
        description='Input arguments for template.'
    )

    # this can change to Union[Function, Workflow]
    template: str = Schema(
        ...,
        description='Template name.'
    )

    dependencies: List[str] = Schema(
        None,
        description='Dependencies are name of other DAG steps which this depends on.'
    )

    loop: Union[str, List[Any]] = Schema(
        None,
        description='List of inputs to loop over.'
    )

    loop_control: LoopControl = Schema(
        None,
        description='Control parameters for loop.'
    )

    @property
    def is_root(self) -> bool:
        """Return true if this function is a root function.

        A root function does not have any dependencies.
        """
        return len(self.dependencies) == 0


class DAG(BaseModel):
    """DAG includes different steps of a directed acyclic graph."""

    name: str = Schema(
        ...,
        description='A unique name for this dag.'
    )

    target: str = Schema(
        None,
        description='Target are one or more names of target tasks to execute in a DAG. '
        'Multiple targets can be specified as space delimited inputs. When a target '
        'is provided only a subset of tasks in DAG that are required to generate '
        'the target(s) will be executed.'
    )

    fail_fast: bool = Schema(
        True,
        description='Stop scheduling new steps, as soon as it detects that one of the'
        ' DAG nodes is failed. Default is True.'
    )

    tasks: List[DAGTask] = Schema(
        ...,
        description='Tasks are a list of DAG steps'
    )
