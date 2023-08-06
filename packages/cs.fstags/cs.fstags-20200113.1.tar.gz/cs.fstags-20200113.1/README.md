Simple filesystem based file tagging and the associated `fstags` command line script.


*Latest release 20200113.1*:
Small docstring updates.

Simple filesystem based file tagging
and the associated `fstags` command line script.

Tags are stored in the file `.fstags` in each directory;
there is a line for each entry in the directory with tags
consisting of the directory entry name and the associated tags.

The tags for a file are the union of its direct tags
and all relevant ancestor tags,
with priority given to tags closer to the file.

For example, a media file for a television episode with the pathname
`/path/to/series-name/season-02/episode-name--s02e03--something.mp4`
might obtain the tags:

    series.title="Series Full Name"
    season=2
    sf
    episode=3
    episode.title="Full Episode Title"

from the following `.fstags` entries:
* tag file `/path/to/.fstags`:
  `series-name sf series.title="Series Full Name"`
* tag file `/path/to/series-name/.fstags`:
  `season-02 season=2`
* tag file `/path/to/series-name/season-02/.fstags`:
  `episode-name--s02e03--something.mp4 episode=3 episode.title="Full Episode Title"`

Tags may be "bare", or have a value.
If there is a value it is expressed with an equals (`'='`)
followed by the JSON encoding of the value.

## Class `FSTags`

A class to examine filesystem tags.

## Class `FSTagsCommand(cs.cmdutils.BaseCommand)`

`fstags` main command line class.


Usage:
    fstags autotag paths...
        Tag paths based on rules from the rc file.
    fstags find [--for-rsync] path {tag[=value]|-tag}...
        List files from path matching all the constraints.
        --direct    Use direct tags instead of all tags.
        --for-rsync Instead of listing matching paths, emit a
                    sequence of rsync(1) patterns suitable for use with
                    --include-from in order to do a selective rsync of the
                    matched paths.
        -o output_format
                    Use output_format as a Python format string to lay out
                    the listing.
                    Default: {filepath}
    fstags ls [--direct] [-o output_format] [paths...]
        List files from paths and their tags.
        --direct    List direct tags instead of all tags.
        -o output_format
                    Use output_format as a Python format string to lay out
                    the listing.
                    Default: {filepath_encoded} {tags}
    fstags mv paths... targetdir
        Move files and their tags into targetdir.
    fstags tag path {tag[=value]|-tag}...
        Associate tags with a path.
        With the form "-tag", remove the tag from the immediate tags.
    fstags tagpaths {tag[=value]|-tag} paths...
        Associate a tag with multiple paths.
        With the form "-tag", remove the tag from the immediate tags.

## Function `infer_tags(name, rules=None)`

Infer `Tag`s from `name` via `rules`. Return a `TagSet`.

`rules` is an iterable of objects with a `.infer_tags(name)` method
which returns an iterable of `Tag`s.

## Function `loadrc(rcfilepath=None)`

Read rc file, return rules.

If `rcfilepath` is `None` default to `'~/.fstagsrc'` (from `RCFILE`).

## Function `main(argv=None)`

Command line mode.

## Class `RegexpTagRule`

A regular expression based `Tag` rule.

## Function `rfilepaths(path, name_selector=None)`

Generator yielding pathnames of files found under `path`.

## Function `rpaths(path, yield_dirs=False, name_selector=None)`

Generator yielding pathnames found under `path`.

## Function `rsync_patterns(paths, top_path)`

Return a list of rsync include lines
suitable for use with the `--include-from` option.

## Class `Tag`

A Tag has a `.name` (`str`) and a `.value`.

The `name` must be a dotted identifier.

A "bare" `Tag` has a `value` of `None`.

## Class `TagChoice(TagChoice,builtins.tuple)`

A "tag choice", an apply/reject flag and a `Tag`,
used to apply changes to a `TagSet`
or as a criterion for a tag search.

Attributes:
* `spec`: the source text from which this choice was parsed,
  possibly `None`
* `choice`: the apply/reject flag
* `tag`: the `Tag` representing the criterion

## Class `TagFile`

A reference to a specific file containing tags.

This manages a mapping of `name` => `TagSet`,
itself a mapping of tag name => tag value.

## Class `TagFileEntry(builtins.tuple)`

TagFileEntry(tagfile, name)

## Class `TaggedPath`

Class to manipulate the tags for a specific path.

## Class `TagSet`

A setlike class associating a set of tag names with values.
A `TagFile` maintains one of these for each name.

### Method `TagSet.__init__(self, *, defaults=None)`

Initialise the `TagSet`.

Parameters:
* `defaults`: a mapping of name->TagSet to provide default values.



# Release Log

*Release 20200113.1*:
Small docstring updates.

*Release 20200113*:
Mirror tags to user.cs.fstags xattr to honour Linux namespace requirements. Add "filesize" to available tag string format (-o option). Small bugfixes.

*Release 20191230*:
Command line: new "find" command to search a file tree based on tags.
Command line: new "mv" command to move a file and its tags.
Command line: Python string formats for "find" and "ls" output.
TaggedPath.autotag: new optional `no_save` parameter, default False, to suppress update of the associated .fstags file.
Inital and untested "mirror tags to xattrs" support.

*Release 20191201*:
New "edit" subcommand to rename files and edit tags.

*Release 20191130.1*:
Initial release: fstags, filesystem based tagging utility.
