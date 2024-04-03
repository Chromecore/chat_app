import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";
import { useApi } from "../hooks";

const emptyChat = (id) => ({
    id,
    name: "loading...",
    empty: true,
});

function Link({ chat }) {
    const url = chat.empty ? "#" : `/chats/${chat.id}`;
    const className = ({ isActive }) => [
        "p-2",
        "hover:bg-zinc-900 hover:text-emerald-500",
        "flex flex-row justify-between",
        isActive ?
            "bg-emerald-500 text-zinc-900 font-bold" :
            ""
    ].join(" ");

    const chatName = ({ isActive }) => (
        (isActive ? "\u00bb " : "") + chat.name
    );

    return (
        <NavLink to={url} className={className}>
            {chatName}
        </NavLink>
    );
}

function LeftNav() {
    const [search, setSearch] = useState("");
    const api = useApi();

    const { data } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
            api.get("/chats")
                .then((response) => response.json())
        ),
    });

    const regex = new RegExp(search.split("").join(".*"));

    const chats = (data?.chats || [1, 2, 3].map(emptyChat)
    ).filter((chat) => (
        search === "" || regex.test(chat.name)
    ));

    return (
        <nav className="flex flex-col border-r-2 border-emerald-500 h-main">
            <div className="flex flex-col overflow-y-scroll border-b-2 border-emerald-500 scrollbar-hide">
                {chats.map((chat) => (
                    <Link key={chat.id} chat={chat} />
                ))}
            </div>
            <div className="p-2">
                <input
                    className="w-36 px-4 py-2 border border-emerald-900 bg-transparent hover:bg-zinc-900"
                    type="text"
                    placeholder="search"
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>
        </nav>
    );
}

export default LeftNav;