# Documentation

The Transformo documentation is build using [Zensical](https://zensical.org/docs/get-started/).
Zensical creates a static website based on file written in Markdown. Users of MkDocs
will feel at home with Zensical as it is the spiritual child of Material for MkDocs.

## Building the documentation

To build the docs locally a [working development setup](developing.md) is needed.
From a terminal environment with the development dependencies activated you can
run the command below to build the documentation:

```sh
$ zensical serve
```

Leave the proces open and open `https://localhost:8000/` in a browser. Zensical will
update the pages when changes to the Markdown files in `docs/` are modified.

## Writing documentionation

The documentation is written in Markdown and occasionally HTML. A number of Markdown addons
are in use, for instance making it possible to create diagrams using Mermaid and maths
using a LaTeX variety. The simplet way to get familiar with the options is to look at
the existing documents and use the same concepts to document new aspects of the software.
