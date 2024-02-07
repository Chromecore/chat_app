import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import "./ChatsPage.css";

function ChatPreview({ chat }) {
    const date = new Date(chat.created_at).toDateString();

    return (
        <Link className="chat-preview" to={`/chats/${chat.id}`}>
            <div>{chat.name}</div>
            <div>
                {chat.user_ids.map((user_id) => (
                    <span key={user_id}>{user_id}, </span>
                ))}
            </div>
            <div>created at: {date}</div>
        </Link>
    );
}

function ChatList({ chats }) {
    return (
        <div>
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
        <div class="message">
            <p>{message.user_id} {date} - {time}</p>
            <p>{message.text}</p>
        </div>
    )
}

function MessageList({ messages }) {
    return (
        <div>
            {messages.map((message) => (
                <Message key={message.id} message={message} />
            ))}
        </div>
    );
}

function ChatMessages() {
    const { chatId } = useParams();
    if (!chatId) {
        return <p>Select a chat</p>;
    }

    const navigate = useNavigate();
    const { data, isloading } = useQuery({
        queryKey: ["messages", chatId],
        queryFn: () => (
            fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
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

    if (isloading) {
        return <p>Loading...</p>;
    }

    if (data?.messages) {
        return <MessageList messages={data.messages} />;
    }

    return <navigate to="/error" />;
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
            <h1>Chats</h1>
            <div class="chats-page">
                {!isloading && data?.chats ?
                    <ChatList chats={data.chats} /> :
                    <h2>NEVER!!!</h2>
                }
                <ChatMessages />
            </div>
        </>
    );
}

export default ChatsPage;