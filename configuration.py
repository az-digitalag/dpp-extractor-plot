#!/usr/bin/env python

"""Contains extractor configuration information
"""

# Setup the name of our extractor. Alphanumeric characters are allows as well as hyphens and underscores '-' and '_'
EXTRACTOR_NAME = ""

# Name of scientific method for this extractor. Leave commented out if it's unknown
#METHOD_NAME = ""

# The version number of the extractor
VERSION = "1.0"

# The extractor description
DESCRIPTION = ""

# The name of the author of the extractor
AUTHOR_NAME = ""

# The email of the author of the extractor
AUTHOR_EMAIL = ""

# Reposity URI of where the source code lives
REPOSITORY = ""

# Citation author for the algorithm
CITATION_AUTHOR = ""

# Citation title for the algorithm
CITATION_TITLE = ""

# Citation year for the algorithm
CITATION_YEAR = ""

# Output variable identifiers. Use a comma separated list if more than one value is returned.
# For example, "variable 1,variable 2" identifies the two variables returned by the extractor.
# If only one name is specified, no comma's are used.
# Note that variable names cannot have comma's in them: use a different separator instead. Also,
# all white space is kept intact; don't add any extra whitespace since it may cause name comparisons
# to fail.
VARIABLE_NAMES = ""

# Uncomment this variable to indicate the extractor is to never write to TERRA REF Geostreams
#NEVER_WRITE_GEOSTREAMS = True

#Uncomment this variable to indicate the extractor is to never write to BETYdb
#NEVER_WRITE_BETYDB = True

# Uncomment this variable to never write CSV files
#NEVER_WRITE_CSV = True
