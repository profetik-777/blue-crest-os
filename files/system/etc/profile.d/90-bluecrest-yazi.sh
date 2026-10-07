# Bash integration: browse with y, return to this shell with t or q.
# User definitions later in ~/.bashrc can override this default.
[ -n "${BASH_VERSION:-}" ] || return 0
case $- in *i*) ;; *) return 0 ;; esac

y() {
    if ! command -v yazi >/dev/null 2>&1; then
        printf '%s\n' 'Yazi setup is pending. Run: systemctl --user start bluecrest-yazi-setup.service' >&2
        return 127
    fi
    local yazi_tmp yazi_cwd yazi_status
    yazi_tmp="$(mktemp -t yazi-cwd.XXXXXX)" || return
    command yazi "$@" --cwd-file="$yazi_tmp"
    yazi_status=$?
    IFS= read -r -d '' yazi_cwd < "$yazi_tmp" || :
    if [ -n "$yazi_cwd" ] && [ "$yazi_cwd" != "$PWD" ] && [ -d "$yazi_cwd" ]; then
        builtin cd -- "$yazi_cwd"
    fi
    command rm -f -- "$yazi_tmp"
    return "$yazi_status"
}
