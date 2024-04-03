function Button(props) {
    const className = [
        props.className || "",
        "border rounded",
        "px-4 py-2 my-4",
        props.disabled ?
            "bg-cyan-600 italic" :
            "border-emerald-500 bg-transparent hover:bg-zinc-900",
    ].join(" ");

    return (
        <button {...props} className={className}>
            {props.children}
        </button>
    );
}

export default Button;
