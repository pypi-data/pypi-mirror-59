function! s:foo() abort
    let x = 'x'
    let y = l:{x}
    echo y
endfunction

call call('s:foo', [])
