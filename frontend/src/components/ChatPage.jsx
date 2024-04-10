import { useQuery } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import NewMessage from "./NewMessage";
import ScrollContainer from "./ScrollContainer";
import { useApi, useAuth, useUser } from "../hooks";

function Message({ message }) {
    const dateDate = new Date(message.created_at);
    const date = dateDate.toDateString();
    const time = dateDate.toLocaleTimeString();

    const user = useUser();
    const { chatId } = useParams();
    const { token } = useAuth();
    const api = useApi(token);

    const onDelete = () => {
        api.remove(`/chats/${chatId}/messages/${message.id}`).then(
            window.location.reload(false)
        )
    };

    const onEdit = () => { }

    return (
        <div className="flex flex-col justify-between border-b border-slate-500 p-2">
            <div className="flex flex-row justify-between">
                <p className="text-lg text-emerald-500">{message.user.username}</p>
                <div className="flex flex-row text-sm">
                    <p className="font-mono text-slate-500 mx-4">{date} - {time}</p>
                    {user.id == message.user.id ?
                        <div>
                            <button className="font-sans text-white border rounded 
                                px-4 bg-transparent hover:bg-zinc-900"
                                onClick={onEdit}>
                                Edit
                            </button>
                            <button className="font-sans text-white border rounded 
                                px-2 bg-rose-600/20 hover:bg-zinc-900"
                                onClick={onDelete}>
                                Delete
                            </button>
                        </div>
                        : <></>
                    }
                </div>
            </div>
            <p className="">{message.text}</p>
        </div>
    )
}

function MessageList({ messages }) {
    return (<>
        <ScrollContainer className="overflow-y-auto">
            {messages.map((message) => (
                <Message key={message.id} message={message} />
            ))}
            <NewMessage />
        </ScrollContainer>
    </>);
}

function Chat() {
    const { chatId } = useParams();
    const { token, isLoggedIn } = useAuth();
    const api = useApi(token);

    const navigate = useNavigate();
    const { data, isloading } = useQuery({
        queryKey: ["messages", chatId, token],
        enabled: isLoggedIn,
        queryFn: () => (
            chatId ?
                api.get(`/chats/${chatId}/messages`)
                    .then((response) => {
                        if (!response.ok) {
                            response.status === 404 ?
                                navigate("/error/404") :
                                navigate("/error");
                        }
                        return response.json()
                    }) : undefined
        ),
    });

    if (!chatId) {
        return <p>Select a chat</p>;
    }

    if (isloading) {
        return <p className="font-bold text-2xl py-4 text-center">Loading...</p>;
    }

    if (data?.messages) {
        return <>
            <MessageList messages={data.messages} />
        </>
    }

    return <h1>Error!</h1>
}

export default Chat;