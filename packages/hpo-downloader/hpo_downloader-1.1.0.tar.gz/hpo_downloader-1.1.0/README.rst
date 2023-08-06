hpo_downloader
===========================================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Python package to download `HPO annotations <https://hpo.jax.org/app/download/annotation>`__
and mapping to `Uniprot ID and AC <https://www.uniprot.org/>`__
and `CAFA4 IDs <https://www.biofunctionprediction.org/cafa/>`__.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install hpo_downloader


Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get
slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Pipeline
----------------------------------------------
The package pipeline is illustrated in the following image:

|pipeline|


Preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the **pre-processing** you have to retrieve the
`uniprot mapping files by asking directly to the Uniprot team
<https://www.uniprot.org/contact>`__
since each mapping is aroung 17GB.
Let's save each file in a directory within this repository called
:code:`"mapping/{month}/idmapping.dat.gz"`.

**Cache for the pre-processing results is available**
**within the python package,**
**so there is no need to retrieve the original**
**files unless you need to fully reproduce the pipeline.**

For each release, we have to retrieve the :code:`"GeneID"`
and the human uniprot_IDs, and we can do so using
`zgrep <http://manpages.ubuntu.com/manpages/trusty/man1/zgrep.1.html>`__.

.. code:: bash

    zgrep "GeneID" mapping/{month}/idmapping.dat.gz > gene_id.tsv
    zgrep "HUMAN" mapping/{month}/idmapping.dat.gz > human_id.tsv

Now we have to map in a non-bijective way uniprot IDs
to GeneIDs on the uniprot ACs.
We can use the package method :code:`non_unique_mapping`.

.. code:: python

    from hpo_downloader.utils import non_unique_mapping
    import pandas as pd

    gene_id = pd.read_csv(
        f"mapping/{month}/gene_id.tsv",
        sep="\t",
        header=None,
        usecols=[0, 2]
    )
    gene_id.columns = ["uniprot_ac", "gene_id"]
    human_id = pd.read_csv(
        f"mapping/{month}/human_ids.tsv",
        sep="\t",
        header=None,
        usecols=[0, 2]
    )
    human_id.columns = ["uniprot_ac", "uniprot_id"]
    non_unique_mapping(gene_id, human_id, "uniprot_ac").to_csv(
        f"hpo_downloader/uniprot/data/{month}.tsv.gz",
        sep="\t",
        index=False
    )

Package usage examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To generate the complete mapping (optionally filtering only
for Uniprot IDs within CAFA4) proceed as follows:

.. code:: python

    from hpo_downloader import mapping

    my_mapping = mapping(
        month="november"
    )

    my_mapping_cafa_only = mapping(
        month="november",
        cafa_only=True
    )

The obtained `pandas DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__
look as follows:

**HPO mappings:**
`October <https://github.com/LucaCappelletti94/hpo_downloader/raw/master/complete_mapping/october.tsv>`__,
`November <https://github.com/LucaCappelletti94/hpo_downloader/raw/master/complete_mapping/november.tsv>`__,
`December <https://github.com/LucaCappelletti94/hpo_downloader/raw/master/complete_mapping/december.tsv>`__

+-----------+------------+--------------+--------------+
|   gene_id | hpo_id     | uniprot_ac   | uniprot_id   |
+===========+============+==============+==============+
|      8192 | HP:0004322 | Q16740       | CLPP_HUMAN   |
+-----------+------------+--------------+--------------+
|      8192 | HP:0001250 | Q16740       | CLPP_HUMAN   |
+-----------+------------+--------------+--------------+
|      8192 | HP:0000786 | Q16740       | CLPP_HUMAN   |
+-----------+------------+--------------+--------------+
|      8192 | HP:0000007 | Q16740       | CLPP_HUMAN   |
+-----------+------------+--------------+--------------+
|      8192 | HP:0000252 | Q16740       | CLPP_HUMAN   |
+-----------+------------+--------------+--------------+

**HPO mappings (CAFA4 only):**
`October (CAFA only) <https://github.com/LucaCappelletti94/hpo_downloader/raw/master/complete_mapping/october_cafa_only.tsv.tsv>`__,
`November (CAFA only) <https://github.com/LucaCappelletti94/hpo_downloader/raw/master/complete_mapping/november_cafa_only.tsv.tsv>`__,
`December (CAFA only) <https://github.com/LucaCappelletti94/hpo_downloader/raw/master/complete_mapping/december_cafa_only.tsv.tsv>`__

+--------------+--------------+-----------+------------+--------------+
| cafa4_id     | uniprot_id   |   gene_id | hpo_id     | uniprot_ac   |
+==============+==============+===========+============+==============+
| T96060000002 | 1433E_HUMAN  |      7531 | HP:0000960 | P62258       |
+--------------+--------------+-----------+------------+--------------+
| T96060000002 | 1433E_HUMAN  |      7531 | HP:0001539 | P62258       |
+--------------+--------------+-----------+------------+--------------+
| T96060000002 | 1433E_HUMAN  |      7531 | HP:0002119 | P62258       |
+--------------+--------------+-----------+------------+--------------+
| T96060000002 | 1433E_HUMAN  |      7531 | HP:0002120 | P62258       |
+--------------+--------------+-----------+------------+--------------+
| T96060000002 | 1433E_HUMAN  |      7531 | HP:0000463 | P62258       |
+--------------+--------------+-----------+------------+--------------+


Author notes
====================================

HPO missing GeneID mappings
------------------------------------
Around 54 to 55 GeneID to Uniprot IDs mapping are currently missing in Uniprot.
I have already signaled this to the Uniprot team
and will update the package accordingly,
if anything is to be made about these.

+----------+-----------------------------+--------------------------------+----------------------------+-------------------------------+
| Month    |   HPO unique missed samples | HPO unique missed percentage   |   HPO total missed samples | HPO total missed percentage   |
+==========+=============================+================================+============================+===============================+
| October  |                          54 | 1.26%                          |                       3076 | 1.86%                         |
+----------+-----------------------------+--------------------------------+----------------------------+-------------------------------+
| November |                          55 | 1.28%                          |                       3162 | 1.91%                         |
+----------+-----------------------------+--------------------------------+----------------------------+-------------------------------+
| December |                          55 | 1.28%                          |                       3162 | 1.91%                         |
+----------+-----------------------------+--------------------------------+----------------------------+-------------------------------+

HPO phenotype ID to CAFA4 Uniprot_IDs missed mappings 
------------------------------------------------------------
A considerable percentage (around 80%) of the HUMAN uniprot IDs used in CAFA4
are not mappable to the HPO phenotype IDs.

+----------+-------------------------------+----------------------------------+------------------------------+---------------------------------+
| Month    |   CAFA4 unique missed samples | CAFA4 unique missed percentage   |   CAFA4 total missed samples | CAFA4 total missed percentage   |
+==========+===============================+==================================+==============================+=================================+
| October  |                         16182 | 79.21%                           |                        16182 | 79.21%                          |
+----------+-------------------------------+----------------------------------+------------------------------+---------------------------------+
| November |                         16184 | 79.22%                           |                        16184 | 79.22%                          |
+----------+-------------------------------+----------------------------------+------------------------------+---------------------------------+
| December |                         16187 | 79.23%                           |                        16187 | 79.23%                          |
+----------+-------------------------------+----------------------------------+------------------------------+---------------------------------+

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/hpo_downloader.png
   :target: https://travis-ci.org/LucaCappelletti94/hpo_downloader
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_hpo_downloader&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_hpo_downloader
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_hpo_downloader&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_hpo_downloader
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_hpo_downloader&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_hpo_downloader
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/hpo_downloader/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/hpo_downloader?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/hpo-downloader.svg
    :target: https://badge.fury.io/py/hpo-downloader
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/hpo-downloader
    :target: https://pepy.tech/badge/hpo-downloader
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/26d152932db342a09ac6b009889255c9
    :target: https://www.codacy.com/manual/LucaCappelletti94/hpo_downloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/hpo_downloader&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |pipeline|  image:: https://github.com/LucaCappelletti94/hpo_downloader/blob/master/HPO%20downloader.png?raw=true
    :alt: Pipeline

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/0cac3687d5c9520e561a/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/hpo_downloader/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/0cac3687d5c9520e561a/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/hpo_downloader/test_coverage
    :alt: Code Climate Coverate
