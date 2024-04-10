import { useApi, useAuth, useUser } from "../hooks";
import { useState } from "react";
import { useParams } from "react-router-dom";
import FormInput from "./FormInput";

function RegularButtons({ message, setEditing, setText }) {
    const { chatId } = useParams();
    const { token } = useAuth();
    const api = useApi(token);

    const onDelete = () => {
        api.remove(`/chats/${chatId}/messages/${message.id}`).then(
            window.location.reload(false)
        )
    };

    const onEdit = () => {
        setEditing(true);
        setText(message.text)
    }

    return <div>
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
    </div>;
}

function EditingButtons({ message, setEditing, setText, text }) {
    const { chatId } = useParams();
    const { token } = useAuth();
    const api = useApi(token);

    const onSave = () => {
        setEditing(false)
        api.put(`/chats/${chatId}/messages/${message.id}`, { text })
    };

    const onCancel = () => {
        setEditing(false)
        setText(message.text)
    }

    return <div>
        <button className="font-sans text-white border rounded 
            px-4 bg-emerald-500/20 hover:bg-ziemeraldnc-900"
            onClick={onSave}>
            Save
        </button>
        <button className="font-sans text-white border rounded 
            px-2 bg-transparent hover:bg-zinc-900"
            onClick={onCancel}>
            Cancel
        </button>
    </div>;
}

function Message({ message }) {
    const dateDate = new Date(message.created_at);
    const date = dateDate.toDateString();
    const time = dateDate.toLocaleTimeString();
    const [editing, setEditing] = useState(false);
    const [text, setText] = useState(message.text);

    const user = useUser();

    return (
        <div className="flex flex-col justify-between border-b border-slate-500 p-2">
            <div className="flex flex-row justify-between">
                <p className="text-lg text-emerald-500">{message.user.username}</p>
                <div className="flex flex-row text-sm">
                    <p className="font-mono text-slate-500 mx-4">{date} - {time}</p>
                    {user.id == message.user.id ?
                        editing ?
                            <EditingButtons key={message.id} message={message}
                                setEditing={setEditing} setText={setText} text={text} /> :
                            <RegularButtons key={message.id} message={message}
                                setEditing={setEditing} setText={setText} />
                        : <></>
                    }
                </div>
            </div>
            {editing ?
                <FormInput
                    name="New Text"
                    type="text"
                    value={text}
                    setter={setText}>

                </FormInput> :
                <p className="">{text}</p>
            }
        </div>
    )
}

export default Message;