"""
Refactors C++ code blocks in markdown files to match 02.code-style.md:
  - adds `using namespace std;` after #include block
  - removes `std::` prefix from cout, cin, string, vector, etc.
Only modifies content inside ```cpp ... ``` fences.
"""

import re
import sys

# Ordered replacements (longest/most-specific first to avoid partial matches)
REPLACEMENTS = [
    # Static member references — must stay as Type::member
    ('std::string::npos',       'string::npos'),
    ('std::string_view::npos',  'string_view::npos'),

    # Types (string_view before string!)
    ('std::string_view',   'string_view'),
    ('std::string',        'string'),
    ('std::vector',        'vector'),
    ('std::array',         'array'),
    ('std::optional',      'optional'),
    ('std::nullopt',       'nullopt'),
    ('std::pair',          'pair'),
    ('std::size_t',        'size_t'),

    # Streams
    ('std::cout',   'cout'),
    ('std::cin',    'cin'),
    ('std::cerr',   'cerr'),
    ('std::endl',   'endl'),

    # Stream manipulators
    ('std::boolalpha',    'boolalpha'),
    ('std::hex',          'hex'),
    ('std::dec',          'dec'),
    ('std::oct',          'oct'),
    ('std::setw',         'setw'),
    ('std::setfill',      'setfill'),
    ('std::setprecision', 'setprecision'),

    # Algorithms
    ('std::sort',      'sort'),
    ('std::equal',     'equal'),
    ('std::find',      'find'),
    ('std::transform', 'transform'),
    ('std::all_of',    'all_of'),
    ('std::any_of',    'any_of'),
    ('std::none_of',   'none_of'),
    ('std::count',     'count'),
    ('std::search',    'search'),
    ('std::copy',      'copy'),
    ('std::remove',    'remove'),
    ('std::replace',   'replace'),
    ('std::max',       'max'),
    ('std::min',       'min'),
    ('std::abs',       'abs'),
    ('std::swap',      'swap'),
    ('std::move',      'move'),

    # String conversion
    ('std::getline',   'getline'),
    ('std::stoi',      'stoi'),
    ('std::stod',      'stod'),
    ('std::stof',      'stof'),
    ('std::stol',      'stol'),
    ('std::stoll',     'stoll'),
    ('std::to_string', 'to_string'),

    # <cctype> functions
    ('std::isalpha', 'isalpha'),
    ('std::isupper', 'isupper'),
    ('std::islower', 'islower'),
    ('std::isdigit', 'isdigit'),
    ('std::isalnum', 'isalnum'),
    ('std::isspace', 'isspace'),
    ('std::ispunct', 'ispunct'),
    ('std::isprint', 'isprint'),
    ('std::iscntrl', 'iscntrl'),
    ('std::toupper', 'toupper'),
    ('std::tolower', 'tolower'),

    # <cstring> functions
    ('std::strlen',   'strlen'),
    ('std::memcpy',   'memcpy'),
    ('std::memset',   'memset'),
    ('std::strcat',   'strcat'),
    ('std::strncat',  'strncat'),
    ('std::strcpy',   'strcpy'),
    ('std::strncpy',  'strncpy'),
    ('std::strcmp',   'strcmp'),
    ('std::strncmp',  'strncmp'),
    ('std::strstr',   'strstr'),
    ('std::strchr',   'strchr'),
    ('std::strrchr',  'strrchr'),

    # <cstdio>
    ('std::printf',   'printf'),
    ('std::sprintf',  'sprintf'),
    ('std::snprintf', 'snprintf'),

    # Wide / Unicode string types
    ('std::u8string_view', 'u8string_view'),
    ('std::u8string',  'u8string'),
    ('std::u16string', 'u16string'),
    ('std::u32string', 'u32string'),
    ('std::wstring',   'wstring'),
    ('std::wcout',     'wcout'),
    ('std::wcin',      'wcin'),

    # Misc stdlib
    ('std::out_of_range',    'out_of_range'),
    ('std::invalid_argument','invalid_argument'),
    ('std::runtime_error',   'runtime_error'),
    ('std::logic_error',     'logic_error'),
    ('std::numeric_limits',  'numeric_limits'),
    ('std::streamsize',      'streamsize'),
    ('std::char_traits',     'char_traits'),
    ('std::allocator',       'allocator'),
    ('std::reverse',         'reverse'),
    ('std::chrono',          'chrono'),
    ('std::iterator',        'iterator'),
    ('std::initializer_list','initializer_list'),
]


def insert_using_namespace(code: str) -> str:
    """Insert `using namespace std;` after the #include block."""
    lines = code.split('\n')

    # Find last #include line
    last_include_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('#include'):
            last_include_idx = i

    if last_include_idx < 0:
        return code  # no includes → skip

    # Skip blank lines right after the last include to find first real code
    first_code_idx = last_include_idx + 1
    while first_code_idx < len(lines) and lines[first_code_idx].strip() == '':
        first_code_idx += 1

    # Build new lines: includes + blank + using + blank + rest
    new_lines = (
        lines[: last_include_idx + 1]
        + ['', 'using namespace std;', '']
        + lines[first_code_idx:]
    )
    return '\n'.join(new_lines)


def transform_block(code: str) -> str:
    """Apply all style transformations to a single cpp block."""
    has_includes = '#include' in code

    # Add `using namespace std;` only to complete programs with #include
    if has_includes and 'using namespace std;' not in code:
        code = insert_using_namespace(code)

    # Apply all std:: → unqualified replacements to ALL blocks
    # (snippets without includes also use unqualified style consistently)
    for old, new in REPLACEMENTS:
        code = code.replace(old, new)

    return code


def process_file(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_block(m):
        header = m.group(1)   # ```cpp [File.cpp] showLineNumbers\n
        body   = m.group(2)   # code content
        footer = m.group(3)   # ```
        return header + transform_block(body) + footer

    result = re.sub(
        r'(```cpp[^\n]*\n)(.*?)(```)',
        replace_block,
        content,
        flags=re.DOTALL,
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)

    changed = content != result
    print(f"{'CHANGED' if changed else 'no change':10s}  {path}")


FILES = [
    'content/02.cpp/37.ascii-characters.md',
    'content/02.cpp/38.unicode-utf.md',
    'content/02.cpp/39.c-strings.md',
    'content/02.cpp/40.std-string-intro.md',
    'content/02.cpp/41.std-string-capacity-access.md',
    'content/02.cpp/42.std-string-modification.md',
    'content/02.cpp/43.std-string-search.md',
]

if __name__ == '__main__':
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for rel in FILES:
        process_file(os.path.join(base, rel))
    print('\nDone.')
