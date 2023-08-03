import { writable, derived } from 'svelte/store';
import { PUBLIC_CLIENT_ID, PUBLIC_CLIENT_SECRET } from '$env/static/public';

export const token = writable();
const get_token = async () => {
	const auth_string = PUBLIC_CLIENT_ID + ':' + PUBLIC_CLIENT_SECRET;
	const auth_base64 = btoa(auth_string);
	const url = 'https://accounts.spotify.com/api/token';
	const headers = {
		Authorization: 'Basic ' + auth_base64,
		'Content-Type': 'application/x-www-form-urlencoded'
	};
	const data = new URLSearchParams({ grant_type: 'client_credentials' });
	const retrievedToken = await fetch(url, {
		method: 'POST',
		headers: headers,
		body: data
	});
	if (retrievedToken.ok) {
		const res1 = await retrievedToken.json();
		token.set(res1['access_token']);
	} else {
		console.log("get token didn't work");
	}
};

get_token();

export const isLoggedIn = writable(false);
export const auth_header = derived(token, ($token) => {
	return { Authorization: 'Bearer ' + $token };
});
