import { useEffect, useState } from "react";
import { useAuth, useUser } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
    const { logout } = useAuth();
    const user = useUser();

    return (
        <div className="max-w-96 mx-auto px-4 py-8">
            <h2 className="text-2xl font-bold py-2">
                Details
            </h2>
            <table className="bg-zinc-900 border-emerald-900 border">
                <tr className="border border-emerald-900">
                    <td>Username:</td>
                    <td className="px-4">{user.username}</td>
                </tr>
                <tr className="border border-emerald-900">
                    <td>Email:</td>
                    <td className="px-4">{user.email}</td>
                </tr>
                <tr className="border border-emerald-900">
                    <td>Member Since:</td>
                    <td className="px-4">{new Date(user.created_at).toLocaleDateString()}</td>
                </tr>
            </table>

            <Button onClick={logout}>
                Logout
            </Button>
        </div>
    );
}

export default Profile;