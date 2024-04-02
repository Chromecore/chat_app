import { NavLink } from "react-router-dom";

function Home() {
    return (
        <div className="max-w-96 mx-auto px-4 py-8">
            Pony Express is a top end chat application with conversations from
            all your favorite movie characters.
            <div>
                <NavLink to="/login">
                    Get Started
                </NavLink>
            </div>
        </div>
    );
}

export default Home;