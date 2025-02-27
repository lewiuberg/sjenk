"""Generate CITATION.cff file for the project."""

from properties import config, settings

citation = {
    "cff-version": "1.2.0",
    "message": "If you use this software, please cite it as below.",
    "title": f"{settings['project']['name'].capitalize()}",
    "abstract": f"{settings.project.description}",
    "authors": [
        {
            "family-names": f"{settings['project']['authors'][0]['name'].split(' ')[-1]}",  # noqa: E501
            "given-names": f"{settings['project']['authors'][0]['name'].split(' ')[0]}",  # noqa: E501
            "orcid": f"{settings['project']['urls']['Orcid']}",
        }
    ],
    "version": f"{settings.project.version}",
    "date-released": f"{config.api.release_date}",
    "repository-code": f"{settings.project.urls.Repository}",
    "license": f"{settings.project.license}",
    "keywords": settings.project.keywords,
}

if __name__ == "__main__":
    from pyconfs import Configuration

    cfg = Configuration.from_dict(citation)
    cfg.as_file(
        "CITATION.cff",
        file_format="yaml",
        sort_keys=False,
    )
