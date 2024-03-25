import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import "./ChatsPage.css";

function ChatPreview({ chat }) {
    const date = new Date(chat.created_at).toDateString();

    return (
        <Link className="chat-preview" to={`/chats/${chat.id}`}>
            <div>{chat.name}</div>
            {/* <div>
                {chat.user_ids.map((user_id) => (
                    <span key={user_id}>{user_id}, </span>
                ))}
            </div> */}
            <div>created at: {date}</div>
        </Link>
    );
}

function ChatList({ chats }) {
    return (
        <div>
            <h1>Chats</h1>
            {chats.map((chat) => (
                <ChatPreview key={chat.id} chat={chat} />
            ))}
        </div>
    );
}

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

function ChatMessages() {
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
        return <MessageList messages={data.messages} />;
    }

    return <h1>Test</h1>//<Navigate to="/error" />;
}

function ChatsPage() {
    const navigate = useNavigate();
    const { data, isloading, error } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
            fetch("http://127.0.0.1:8000/chats")
                .then((response) => {
                    if (!response.ok) {
                        response.status === 404 ?
                            navigate("/error/404") :
                            navigate("/error");
                    }
                    return response.json()
                })
        ),
    });

    if (error) {
        return <Navigate to="/error" />
    }

    return (
        <>
            <div className="chats-page">
                {!isloading && data?.chats ?
                    <ChatList chats={data.chats} /> :
                    <></>
                }
                <ChatMessages />
            </div>
        </>
    );
}

export default ChatsPage;