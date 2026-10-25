#!/usr/bin/python3

import asyncio
import os
import re
from html import escape

from card_layout import language_markup

import aiohttp

from github_stats import Stats


################################################################################
# Helper Functions
################################################################################


def generate_output_folder() -> None:
    """
    Create the output folder if it does not already exist
    """
    if not os.path.isdir("generated"):
        os.mkdir("generated")


################################################################################
# Individual Image Generation Functions
################################################################################


async def generate_overview(s: Stats) -> None:
    """
    Generate an SVG badge with summary statistics
    :param s: Represents user's GitHub statistics
    """
    print("\n🎨 Generating overview image...", flush=True)
    with open("templates/overview.svg", "r") as f:
        output = f.read()

    output = output.replace("{{ name }}", escape(await s.name))
    output = re.sub("{{ stars }}", f"{await s.stargazers:,}", output)
    output = re.sub("{{ forks }}", f"{await s.forks:,}", output)
    output = re.sub("{{ contributions }}", f"{await s.total_contributions:,}", output)
    changed = (await s.lines_changed)[0] + (await s.lines_changed)[1]
    output = re.sub("{{ lines_changed }}", f"{changed:,}", output)
    output = re.sub("{{ views }}", f"{await s.views:,}", output)
    output = re.sub("{{ repos }}", f"{len(await s.repos):,}", output)

    generate_output_folder()
    with open("generated/overview.svg", "w") as f:
        f.write(output)
    print("✅ Overview image generated", flush=True)


async def generate_languages(s: Stats) -> None:
    """
    Generate an SVG badge with summary languages used
    :param s: Represents user's GitHub statistics
    """
    print("\n🎨 Generating languages image...", flush=True)
    with open("templates/languages.svg", "r") as f:
        output = f.read()

    progress, lang_list, summary = language_markup(await s.languages)
    output = output.replace("{{ progress }}", progress)
    output = output.replace("{{ lang_list }}", lang_list)
    output = output.replace("{{ language_summary }}", summary)

    generate_output_folder()
    with open("generated/languages.svg", "w") as f:
        f.write(output)
    print("✅ Languages image generated", flush=True)


################################################################################
# Main Function
################################################################################


async def main() -> None:
    """
    Generate all badges
    """
    print("🚀 Starting GitHub Stats Generator", flush=True)
    print("=" * 50, flush=True)
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        # access_token = os.getenv("GITHUB_TOKEN")
        raise Exception("A personal access token is required to proceed!")
    user = os.getenv("GITHUB_ACTOR")
    if user is None:
        raise RuntimeError("Environment variable GITHUB_ACTOR must be set.")
    exclude_repos = os.getenv("EXCLUDED")
    excluded_repos = (
        {x.strip() for x in exclude_repos.split(",")} if exclude_repos else None
    )
    exclude_langs = os.getenv("EXCLUDED_LANGS")
    excluded_langs = (
        {x.strip() for x in exclude_langs.split(",")} if exclude_langs else None
    )
    # Convert a truthy value to a Boolean
    raw_ignore_forked_repos = os.getenv("EXCLUDE_FORKED_REPOS")
    ignore_forked_repos = (
        not not raw_ignore_forked_repos
        and raw_ignore_forked_repos.strip().lower() != "false"
    )
    print(f"\n⚙️  Configuration:", flush=True)
    print(f"   User: {user}", flush=True)
    print(f"   Excluded repos: {len(excluded_repos) if excluded_repos else 0}", flush=True)
    print(f"   Excluded languages: {len(excluded_langs) if excluded_langs else 0}", flush=True)
    print(f"   Ignore forked repos: {ignore_forked_repos}", flush=True)
    print(flush=True)
    
    async with aiohttp.ClientSession() as session:
        s = Stats(
            user,
            access_token,
            session,
            exclude_repos=excluded_repos,
            exclude_langs=excluded_langs,
            ignore_forked_repos=ignore_forked_repos,
        )
        await asyncio.gather(generate_languages(s), generate_overview(s))
    
    print("\n" + "=" * 50, flush=True)
    print("🎉 GitHub Stats generation completed successfully!", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
