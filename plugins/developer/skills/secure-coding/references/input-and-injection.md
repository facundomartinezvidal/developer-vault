# Input handling and injection

Hand-written summary of common practice, using OWASP Top 10, OWASP Cheat Sheets and CWE categories. Not generated from the vault. Check current guidance and the framework's documentation for specifics.

## Contents

- Validation versus encoding
- SQL and NoSQL injection (CWE-89)
- Command injection (CWE-78)
- Cross-site scripting (CWE-79)
- Path traversal and uploads (CWE-22, CWE-434)
- SSRF (CWE-918)
- Unsafe deserialization and parsers (CWE-502, CWE-611)
- Template and log injection
- Regular expression DoS (CWE-1333)
- Dangerous functions by language family

## Validation versus encoding

Validate at the boundary: type, length, range, format, and allowlists over denylists. It rejects bad data early and improves reliability. It doesn't make data safe for every destination, since a valid name like `O'Brien` is still dangerous in concatenated SQL. So separate data from code at the sink. Validate on the server: client checks are only for user experience. Canonicalize before you check, and don't transform after it.

## SQL and NoSQL injection

Use bound parameters for all values. ORMs are safe until you use raw fragments, so look for string interpolation in `raw`, `where` and `order by`. Identifiers like column names can't be bound, so map from an allowlist. In document stores, don't pass client JSON directly as a filter, since an operator object like `{"$ne": null}` changes its meaning. Validate that a value is a scalar.

## Command injection

Avoid calling a process if a library does the job. Otherwise use an API with an argument array and no shell. Input starting with `-` can still inject options, so use `--` where supported. Allowlist the arguments, and consider what the program itself can do, such as read files or fetch URLs.

## Cross-site scripting

Keep the framework's auto-escaping on. Escaping depends on context: HTML body, attribute, JavaScript, URL or CSS each differ. Danger points are `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `|safe` or `html_safe`, and building URLs from input (check the scheme so `javascript:` is refused). For user-supplied rich text, sanitize with a maintained library such as DOMPurify. A Content Security Policy is an additional layer.

## Path traversal and uploads

Don't build paths from user input. Generate a name and store the mapping. If you must, resolve the final path, following symlinks, and check it's under the base directory. For uploads: limit size, verify the type by content instead of trusting the extension or `Content-Type`, store outside the web root or in object storage, serve from another origin or with `Content-Disposition: attachment`, and be careful with archives (zip slip, zip bombs) and with image or document processors.

## SSRF

When a server fetches a URL from input, an attacker can reach internal services and cloud metadata endpoints. Prefer allowlisting hosts. Otherwise resolve DNS, and block private, loopback and link-local ranges including IPv6. Re-validate on redirects, or disable them. Check for DNS rebinding by connecting to the checked IP. Keep the fetcher's network permissions low.

## Unsafe deserialization and parsers

Native object formats can execute code when loaded: `pickle`, YAML unsafe loaders, Java serialization, PHP `unserialize`, Ruby `Marshal`, and .NET `BinaryFormatter`. Use data-only formats such as JSON and validate them against a schema. Turn off external entities in XML parsers. Treat prototype pollution in JavaScript as a related risk when merging objects from input.

## Template and log injection

Don't build templates from user input, only values passed to a fixed template. In logs, encode line breaks so that entries can't be forged, and don't log secrets. In generated CSV files, cells beginning with `=`, `+`, `-` or `@` can run as formulas in spreadsheets.

## Regular expression DoS

Nested quantifiers such as `(a+)+` can take exponential time on crafted input in backtracking engines. Limit input length, simplify the pattern, or use a linear-time engine such as RE2. More generally, limit sizes and nesting of anything parsed from input.

## Dangerous functions by language family

Examples only, not a complete list. Look for the same concept in the language at hand.

| Family | Code execution | Shell | Unsafe load |
|---|---|---|---|
| Python | `eval`, `exec` | `os.system`, `subprocess(shell=True)` | `pickle`, `yaml.load` |
| JavaScript/TypeScript | `eval`, `new Function`, `vm` | `child_process.exec` | prototype-polluting merges |
| Ruby | `eval`, `send` with input | backticks, `system` with a string | `Marshal.load`, `YAML.load` |
| PHP | `eval`, `include` with input | `shell_exec`, `system` | `unserialize` |
| Java/Kotlin | reflection with input, script engines | `Runtime.exec` with a string | `ObjectInputStream` |
| C#/.NET | dynamic compilation | `Process.Start` with a shell | `BinaryFormatter` |
| Go | `html/template` bypass types | `exec.Command("sh","-c",…)` | `text/template` for HTML |
| Rust | `unsafe` blocks | `Command` running `sh -c` | FFI boundaries |
| C/C++ | format strings, `gets`, `strcpy` | `system`, `popen` | unchecked buffers |
| SQL procedures | dynamic `EXEC` | `xp_cmdshell` | |
