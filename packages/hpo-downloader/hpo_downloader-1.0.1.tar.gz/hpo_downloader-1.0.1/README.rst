hpo_downloader
===========================================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package to download HPO annotations

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install hpo_downloader

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|


Usage examples
-----------------------------------------------
The library offers mainly two methods:

Map HPO ids to Uniprot ids
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To map the available HPO ids to Uniprot Ids (**when possible, not all geneIds used in HPO map to Uniprot Ids**) use the following method:

.. code:: python

    from hpo_downloader import map_phenotype_to_uniprot
    phenotype_to_uniprot = map_phenotype_to_uniprot(
        cafa4_only=False # To not filter for uniprot_ids present only in CAFA4
    )

    phenotype_to_uniprot_cafa4_only = map_phenotype_to_uniprot(
        cafa4_only=True # To filter for uniprot_ids present only in CAFA4
    )

The resulting dataframe will look like this:

+---------------+---------------+
| Uniprot\_ID   | HPO-Term-ID   |
+===============+===============+
| A2MG\_HUMAN   | HP:0410054    |
+---------------+---------------+
| A2MG\_HUMAN   | HP:0001425    |
+---------------+---------------+
| A2MG\_HUMAN   | HP:0001300    |
+---------------+---------------+
| A2MG\_HUMAN   | HP:0000006    |
+---------------+---------------+
| A2MG\_HUMAN   | HP:0000726    |
+---------------+---------------+
| A2MG\_HUMAN   | HP:0002423    |
+---------------+---------------+
| A2MG\_HUMAN   | HP:0002185    |
+---------------+---------------+

The `last version with all the mapping is available here <https://raw.githubusercontent.com/LucaCappelletti94/hpo_downloader/master/phenotype_to_uniprot.tab>`_ in tab format.
Similarly, `the CAFA4 only mapping is available here <https://raw.githubusercontent.com/LucaCappelletti94/hpo_downloader/master/phenotype_to_uniprot_cafa4_only.tab>`_ in tab format.

**N.B.: CURRENTLY 55 gene IDs (1.28% of total) are not mapped by uniprot to curresponding uniprot IDs**

**N.B.: CURRENTLY 16187 CAFA4 Uniprot_Ids (79.23% of total) are not mapped by uniprot to curresponding HPO IDs**

Download HPO Phenotype annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To download the phenotype annotations you can use the following method:

.. code:: python

    from hpo_downloader import get_phenotype_annotations

    annotations = get_phenotype_annotations()

The resulting dataframe will look like this:

+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+
| DB         | DB\_Object\_ID   | DB\_Name                         | Qualifier   | HPO\_ID      | DB\_Reference   | Evidence\_Code   | Onset modifier   | Frequency   | Sex   | Modifier   | Aspect                           | Date\_Created              | Assigned\_By   |
+============+==================+==================================+=============+==============+=================+==================+==================+=============+=======+============+==================================+============================+================+
| DECIPHER   | 1                | Wolf-Hirschhorn Syndrome         |             | HP:0001249   | DECIPHER:1      | IEA              |                  |             |       | P          | WOLF-HIRSCHHORN SYNDROME         | HPO:skoehler[2013-05-29]   |                |
+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+
| DECIPHER   | 1                | Wolf-Hirschhorn Syndrome         |             | HP:0001250   | DECIPHER:1      | IEA              |                  |             |       | P          | WOLF-HIRSCHHORN SYNDROME         | HPO:skoehler[2013-05-29]   |                |
+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+
| DECIPHER   | 1                | Wolf-Hirschhorn Syndrome         |             | HP:0001252   | DECIPHER:1      | IEA              |                  |             |       | P          | WOLF-HIRSCHHORN SYNDROME         | HPO:skoehler[2013-05-29]   |                |
+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+
| DECIPHER   | 1                | Wolf-Hirschhorn Syndrome         |             | HP:0001518   | DECIPHER:1      | IEA              |                  |             |       | P          | WOLF-HIRSCHHORN SYNDROME         | HPO:skoehler[2013-05-29]   |                |
+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+
| DECIPHER   | 14               | Prader-Willi syndrome (Type 1)   |             | HP:0000135   | DECIPHER:14     | IEA              |                  |             |       | P          | PRADER-WILLI SYNDROME (TYPE 1)   | HPO:skoehler[2013-05-29]   |                |
+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+
| DECIPHER   | 14               | Prader-Willi syndrome (Type 1)   |             | HP:0001249   | DECIPHER:14     | IEA              |                  |             |       | P          | PRADER-WILLI SYNDROME (TYPE 1)   | HPO:skoehler[2013-05-29]   |                |
+------------+------------------+----------------------------------+-------------+--------------+-----------------+------------------+------------------+-------------+-------+------------+----------------------------------+----------------------------+----------------+


Download CAFA4 Ids
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To download the CAFA4 and Uniprot Ids mapping use the following method:

.. code:: python

    from hpo_downloader import load_cafa4_uniprot_ids

    cafa_mapping = load_cafa4_uniprot_ids()

The resulting dataframe will look like this:

+----------------+----------------+
| CAFA\_Id       | Uniprot\_Id    |
+================+================+
| T96060000001   | 1433B\_HUMAN   |
+----------------+----------------+
| T96060000002   | 1433E\_HUMAN   |
+----------------+----------------+
| T96060000003   | 1433F\_HUMAN   |
+----------------+----------------+
| T96060000004   | 1433G\_HUMAN   |
+----------------+----------------+
| T96060000005   | 1433S\_HUMAN   |
+----------------+----------------+
| T96060000006   | 1433T\_HUMAN   |
+----------------+----------------+
| T96060000007   | 1433Z\_HUMAN   |
+----------------+----------------+
| T96060000008   | 1A01\_HUMAN    |
+----------------+----------------+
| T96060000009   | 1A02\_HUMAN    |
+----------------+----------------+
| T96060000010   | 1A03\_HUMAN    |
+----------------+----------------+


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

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/0cac3687d5c9520e561a/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/hpo_downloader/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/0cac3687d5c9520e561a/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/hpo_downloader/test_coverage
    :alt: Code Climate Coverate