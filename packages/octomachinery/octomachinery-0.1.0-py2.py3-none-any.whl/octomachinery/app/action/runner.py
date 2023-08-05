"""Octomachinery CLI runner for GitHub Action environments."""

import asyncio
import logging
import typing

from aiohttp.client import ClientSession

# pylint: disable=relative-beyond-top-level
from ...github.entities.action import GitHubAction
# pylint: disable=relative-beyond-top-level
from ...github.errors import GitHubActionError
# pylint: disable=relative-beyond-top-level
from ...github.models.action_outcomes import (
    ActionSuccess, ActionNeutral, ActionFailure,
)
# pylint: disable=relative-beyond-top-level
from ..config import BotAppConfig
# pylint: disable=relative-beyond-top-level
from ..routing.webhooks_dispatcher import (
    route_github_action_event,
)
# pylint: disable=relative-beyond-top-level
from ..runtime.context import RUNTIME_CONTEXT


logger = logging.getLogger(__name__)


async def process_github_action(config):
    """Schedule GitHub Action event for processing."""
    RUNTIME_CONTEXT.config = config  # pylint: disable=assigning-non-slot
    logger.info('Processing GitHub Action event...')

    async with ClientSession() as http_client_session:
        github_action = GitHubAction(
            metadata=config.action,
            http_session=http_client_session,
            user_agent=config.github.user_agent,
        )
        logger.info('GitHub Action=%r', config.action)

        await route_github_action_event(github_action)
    return ActionSuccess('GitHub Action has been processed')


def run(*, config: typing.Optional[BotAppConfig] = None) -> None:
    """Start up a server using CLI args for host and port."""
    if config is None:
        config = BotAppConfig.from_dotenv()

    logging.basicConfig(
        level=logging.DEBUG
        if config.runtime.debug  # pylint: disable=no-member
        else logging.INFO,
    )

    try:
        processing_outcome = asyncio.run(process_github_action(config))
    except GitHubActionError as action_error:
        action_error.terminate_action()
    except KeyboardInterrupt:
        ActionNeutral('Action processing interrupted by user').raise_it()
    except Exception:  # pylint: disable=broad-except
        err_msg = 'Action processing failed unexpectedly'
        logger.exception(err_msg)
        ActionFailure(err_msg).raise_it()
    else:
        processing_outcome.raise_it()
