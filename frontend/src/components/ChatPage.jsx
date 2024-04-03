import { useQuery } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import NewMessage from "./NewMessage";
import ScrollContainer from "./ScrollContainer";

function Message({ message }) {
    const dateDate = new Date(message.created_at);
    const date = dateDate.toDateString();
    const time = dateDate.toLocaleTimeString();

    return (
        <div className="flex flex-col justify-between border-b border-slate-500 p-2">
            <div className="flex flex-row justify-between">
                <p className="text-lg text-emerald-500">{message.user.username}</p>
                <p className="font-mono text-sm text-slate-500">{date} - {time}</p>
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

    const navigate = useNavigate();
    const { data, isloading } = useQuery({
        queryKey: ["messages", chatId],
        queryFn: () => (
            chatId ?
                fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
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