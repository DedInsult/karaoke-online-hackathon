function similarity(a, b) {
    let count = a.filter(value => b.includes(value))
    return count.length / a.length * 100
}