FROM python:3-onbuild

MAINTAINER Steve Engledow <steve.engledow@proxama.com>

# Run unit tests by default
CMD ["python", "-m", "unittest"]
