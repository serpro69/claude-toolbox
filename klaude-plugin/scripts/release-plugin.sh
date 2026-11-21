#!/usr/bin/env bash
# The caller supplies the physical root of the plugin whose hook Claude ran.
is_release_plugin() {
    local root=$1 version_dir releases home
    version_dir=${root%/*}
    releases=${version_dir%/*}
    [[ ${root##*/} == klaude-plugin && ${releases##*/} == releases ]] || return 1

    home=${KK_HOME:-${XDG_DATA_HOME:-"$HOME/.local/share"}/kk}
    # Plain Claude can load a custom-home release before the first install
    # has published its dispatcher. Its journal and payload still identify
    # the layout, including older releases retained for running sessions.
    [[ "$releases" -ef "$home/releases" ]] ||
        [[ -f "${releases%/*}/state.json" && -f "$version_dir/kk/payload.json" ]]
}
