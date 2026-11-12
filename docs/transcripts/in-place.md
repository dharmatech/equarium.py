# In place and on every save

`--in-place` runs a script and writes its results into it, as `#> `
comments under each statement. `--watch` does that now, and again every
time you save the script, until you stop it with Ctrl-C:

```bash
uv run python -m equarium.transcript --watch docs/transcripts/basics.py
```

Keep it running in a terminal, and edit the script in VS Code. Each
save prints a line in the terminal, such as
`basics.py: ran, results written`, and VS Code shows the file with its
new results. Since the results are comments, the editor's syntax
highlighting and tools keep working.

Before every run, the old `#> ` lines are dropped, so old results never
run or pile up. Each run under `--watch` is a fresh Python, so a change
to a module the script imports shows up too.

## Your code is safe

The script is written only when that's safe:

- **Not when it doesn't parse,** as in the middle of an edit. It's left
  as it is until it does.
- **Not when it changed while it ran.** A save you made meanwhile isn't
  overwritten, and that save runs it again.
- **After an error,** the results go up to the error, and the lines
  after it stay as they are.

The results in the file have no colors, since color codes would show up
in it as `\x1b[32m`.

If you keep typing while a run finishes, VS Code may say at your next
save that the file on disk is newer. Choose to overwrite it: the only
difference is the `#> ` lines, which the next run writes again.

## If VS Code doesn't show the new results

If the terminal says `results written` but VS Code shows the new results
only after you click away and back, VS Code isn't seeing changes on
disk. On Linux its file watching needs inotify instances, 128 per user
by default, and many editor windows and tool sessions can use them up.
VS Code's log then shows `EMFILE: too many open files`.

Restarting the programs holding them frees them. To raise the limit:

```bash
sudo sysctl fs.inotify.max_user_instances=1024
```

And to keep it after a reboot:

```bash
echo 'fs.inotify.max_user_instances = 1024' | sudo tee /etc/sysctl.d/60-inotify-instances.conf
```
