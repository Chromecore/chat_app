import { useAuth, useUser } from "../hooks";
import { NavLink } from "react-router-dom";

function NavItem({ to, name, right }) {
    const className = [
        "border-emerald-500",
        "py-2 px-4",
        "hover:bg-emerald-950",
        right ? "border-l-2" : "border-r-2"
    ].join(" ")

    const getClassName = ({ isActive }) => (
        isActive ? className + " bg-slate-800" : className
    );

    return (
        <NavLink to={to} className={getClassName}>
            {name}
        </NavLink>
    );
}

function AuthenticatedNavItems() {
    const user = useUser();

    return (
        <>
            <NavItem to="/" name="Pony Epxress" />
            <div className="flex-1" />
            <NavItem to="/profile" name={user?.username} right />
        </>
    );
}

function UnauthenticatedNavItems() {
    return (
        <>
            <NavItem to="/" name="Pony Epxress" />
            <div className="flex-1" />
            <NavItem to="/login" name="login" right />
        </>
    );
}

function TopNav() {
    const { isLoggedIn } = useAuth();

    return (
        <nav className="flex flex-row border-b-4 border-emerald-500">
            {isLoggedIn ?
                <AuthenticatedNavItems /> :
                <UnauthenticatedNavItems />
            }
        </nav>
    );
}

export default TopNav;