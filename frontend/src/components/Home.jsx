import { NavLink } from "react-router-dom";

function Home() {
    const className = [
        "border rounded",
        "px-4 py-2 my-4",
        "border-lgrn bg-transparent hover:bg-slate-800",
    ].join(" ");

    return (
        <div className="max-w-4/5 mx-auto text-center px-4 py-8">
            Pony Express is a top end chat application with conversations from
            all your favorite movie characters.
            <div className={className}>
                <NavLink to="/login">
                    Get Started
                </NavLink>
            </div>
        </div>
    );
}

export default Home;