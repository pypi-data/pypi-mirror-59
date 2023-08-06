# -*- coding: utf-8 -*-

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='tests/docs/basic/')
def test_build_html(app, status, warning):
    app.builder.build_all()


@with_app(buildername='singlehtml', srcdir='tests/docs/basic/')
def test_build_singlehtml(app, status, warning):
    app.builder.build_all()
    html = (app.outdir / 'index.html').read_text()
    assert ('<p>A sphinx extension to include jinja based templates based '
            'documentation into a sphinx doc</p>') in html
    assert '<p>b</p>' in html
    assert '<p>second:a = b</p>' in html


@with_app(buildername='latex', srcdir='tests/docs/basic/')
def test_build_latex(app, status, warning):
    app.builder.build_all()


@with_app(buildername='epub', srcdir='tests/docs/basic/')
def test_build_epub(app, status, warning):
    app.builder.build_all()


@with_app(buildername='json', srcdir='tests/docs/basic/')
def test_build_json(app, status, warning):
    app.builder.build_all()
