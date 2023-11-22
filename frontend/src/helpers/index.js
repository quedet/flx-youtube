const debounce = (callback, delay=5) => {
    let timeoutId = null;

    return () => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(callback, delay);
    };
};

module.exports = debounce;