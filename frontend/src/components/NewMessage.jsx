import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useParams } from "react-router-dom";
import { useApi } from "../hooks";

function NewMessage() {
    const queryClient = useQueryClient();
    const api = useApi();
    const [text, setText] = useState("");
    const { chatId } = useParams();

    const mutation = useMutation({
        mutationFn: () => (
            api.post(
                `/chats/${chatId}/messages`,
                { text },
            ).then((response) => response.json())
        ),
        onSuccess: (data) => {
            queryClient.invalidateQueries({
                queryKey: ["chats"],
            });
        },
    });

    const onSubmit = (e) => {
        mutation.mutate();
    };

    return (
        <form onSubmit={onSubmit} className="flex flex-row py-2">
            <input className="w-full border rounded bg-transparent px-2 py-1"
                placeholder="New Message" value={text}
                onChange={(e) => setText(e.target.value)} />
            <button className="border rounded px-4 py-2 bg-emerald-500 hover:bg-zinc-900">
                Send
            </button>
        </form>
    );
}

export default NewMessage;