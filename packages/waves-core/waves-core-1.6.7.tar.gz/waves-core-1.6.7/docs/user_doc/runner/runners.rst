.. _runner-admin-label:

=========================
Computing infrastructures
=========================

Computing infrastructures shortly named "Runner" are the entry point where you can setup different configuration on where and how services' jobs
may be run.


Environment list
================

    List all currently registered environment available on your WAVES application, you may add / edit / remove (cautiously).

    .. figure:: backoffice/runner-list.png
        :align: center
        :width: 90%
        :figclass: thumbnail

        List of environment already set

Environment details
===================

Main panel
----------
    .. figure:: backoffice/runner-detail.png
        :align: center
        :width: 90%
        :figclass: thumbnail

        Detail admin page

    On detailed environment page, configure some descriptive parameters :

    - **Label**: The displayed runner name used in front / back-office for reference (used some time in templates)
    - **Run on**: Specify here which WAVES-core adapter is used for running jobs
    - **Connexion string**: The used connexion string (readonly)
    - **Reset related services**: When checked, upon save, all related services configuration is reset to defaults parameters

    .. CAUTION::
        These services are now in stage 'Draft'

.. _environment-set-up:

Environment setup
-----------------
    .. figure:: backoffice/runner-param.png
        :align: center
        :width: 90%
        :figclass: thumbnail

        Computing infrastructure init parameters

    You can set 'run configuration' values such as login/password, destination host, etc... depending of the WAVES adapter you select in previous panel

    .. note::
        You can't set up your environment till you have saved your initial configuration once.

        On the top left corner, once configured, a button allows you to test your parameters in order to verify if WAVES-core can actually connect to the Computing infrastructure.

    .. hint::
        You can prevent subsequent service(s) to override a value in their own configuration administration page, by checking 'Prevent override' related checkbox.

Running services
----------------

    Down the page, there is a list of current services which use this Computing infrastructure.

