# Dungeon excavator web interface

This is a Flask blueprint for a web interface for the
[dungeon mapper](https://github.com/detly/dungeon). Run:

```
webcavate
```

...and load `http://localhost:5050/` in a browser. (If you haven't installed the
package via `pip` you can use `python -m webcavate`.)

You can change the port that the web app runs on using the `-p` option, and if
you want to access the interface from another machine, use `-a 0.0.0.0` (or some
other address to bind to).

## Sass

Run

```
compass compile --sass-dir=webcavate/sass/ --css-dir=webcavate/static/css/
```

to compile the CSS.
