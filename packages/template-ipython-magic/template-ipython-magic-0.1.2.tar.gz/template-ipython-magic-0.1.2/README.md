# Template IPython magics 🎩

This package provides simple IPython magics to render cells as templates in a variety of different templating languages. It currently supports [Mako][] and [Jinja2][].

[Mako]: https://www.makotemplates.org/
[Jinja2]: https://jinja.palletsprojects.com/

To use it, first install the package from PyPI, along with at least one of the supported templating languages. E.g. using `pipenv` (everyone should use [`pipenv`][pipenv]):

```shell
pipenv install template-ipython-magic jinja2 mako
```

[pipenv]: https://pipenv.readthedocs.io/en/latest/

In your notebook, load the `template_magic` module:


```python
%load_ext template_magic
```

Note that the available templating languages are detected at the point of loading the extension, and each magic only enabled if the appropriate package is found. If neither Jinja2 or Mako are installed, there will be no magics!

Now you can use `%jinja` as a line magic within any code block, with access to all variables in scope. The result is formatted as Markdown:


```python
import sys

%jinja Hello from **Jinja** on Python {{sys.version_info.major}}.{{sys.version_info.minor}}! 🐍
```


Hello from **Jinja** on Python 3.8! 🐍


If you prefer, `%mako` is also available:


```python
import datetime
now = datetime.datetime.now()

%mako Hello from *Mako* at ${now.strftime('%I:%M %p')}... ⏰
```


Hello from *Mako* at 08:39 PM... ⏰


Cell magics are also available for each language, which lets you render the entire cell as a template for convenient report generation:


```python
%%jinja

{%- for x in ['spam'] * 7 + ['eggs', 'spam'] %}
- {% if loop.last %}and {% endif %}{{x}}{%if not loop.last %},{% endif %}
{%- endfor %}
```



- spam,
- spam,
- spam,
- spam,
- spam,
- spam,
- spam,
- eggs,
- and spam

