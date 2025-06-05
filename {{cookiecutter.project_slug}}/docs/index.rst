Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   {% if cookiecutter.include_utils_lib == 'y' %}utils{% endif %}
   {% if cookiecutter.include_version_management == 'y' %}version{% endif %}
   developer_guide
   {% if cookiecutter.include_dependabot == 'y' %}dependabot{% endif %}
   {% if cookiecutter.include_docker == 'y' %}docker{% endif %}
   api/modules
   contributing
   {% if cookiecutter.create_author_file == 'y' %}authors{% endif %}
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
