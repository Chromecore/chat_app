import { useQuery } from "react-query";
import { useNavigate, useParams } from "react-router-dom";

function Message({ message }) {
    const dateDate = new Date(message.created_at);
    const date = dateDate.toDateString();
    const time = dateDate.toLocaleTimeString();

    return (
        <div className="message">
            <p>{message.user_id} {date} - {time}</p>
            <p>{message.text}</p>
        </div>
    )
}

function MessageList({ messages }) {
    return (
        <div>
            <h1>Messages</h1>
            {messages.map((message) => (
                <Message key={message.id} message={message} />
            ))}
        </div>
    );
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
        return <p>Loading...</p>;
    }

    if (data?.messages) {
        return <>
            <MessageList messages={data.messages} />;
            <div className="flex flex-col py-2">
                <label className="text-s text-gray-400" >
                    Send
                </label>
                <input className="border rounded bg-transparent px-2 py-1" />
            </div>
        </>
    }

    return <h1>Error!</h1>
}

export default Chat;