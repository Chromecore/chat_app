import { useQuery } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import NewMessage from "./NewMessage";
import ScrollContainer from "./ScrollContainer";
import { useApi, useAuth } from "../hooks";
import Message from "./Message";

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