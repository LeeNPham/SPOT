<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import { PUBLIC_CLIENT_ID, PUBLIC_CLIENT_SECRET } from '$env/static/public';
	import { onMount } from 'svelte';
	import axios from 'axios';

	function get_token() {
		let auth_string = PUBLIC_CLIENT_ID + ':' + PUBLIC_CLIENT_SECRET;
		let auth_bytes = `b'${auth_string}'`;
		const auth_base64 = btoa(auth_bytes); //might need to change this to auth_string?
		console.log(auth_base64);
		const url = 'https://accounts.spotify.com/api/token';
		const headers = {
			Authorization: 'Basic ' + auth_base64,
			'Content-Type': 'application/x-www-form-urlencoded'
		};
		const data = new URLSearchParams({ grant_type: 'client_credentials' });
		return axios
			.post(url, data, { headers })
			.then(async (response) => {
				const token = response.data.access_token;
				return token;
			})
			.catch((error) => {
				console.error('Error fetching token:', error);
				return null;
			});
	}

	function search_for_artist(auth_header, artist_name) {
		let url = 'https://api.spotify.com/v1/search';
		let headers = auth_header;
		let query = `?q=${artist_name}&type=artist&limit=1`;
		let query_url = url + query;

		return axios
			.get(query_url, { headers })
			.then(async (response) => {
				const artist_responsefromsearch = response.data;
				console.log(artist_responsefromsearch);
			})
			.catch((error) => {
				console.error('No Artist with this name exist', error);
				return null;
			});
	}

	onMount(async () => {
		console.log(PUBLIC_CLIENT_ID);
		console.log(PUBLIC_CLIENT_SECRET);
		let token = await get_token();
		const auth_header = { Authorization: 'Bearer ' + token };
		let artist_res = await search_for_artist(auth_header, 'ACDC');
		console.log(artist_res);
		//try to grab a list of songs to generally display such as top tracks or playlists?
		//refer to main.py to convert get call into a fetch to be used in onmount
		//create a stores value for your consistently used access token
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>
		<span class="welcome">
			<picture>
				<source srcset={welcome} type="image/webp" />
				<img src={welcome_fallback} alt="Welcome" />
			</picture>
		</span>

		to your new<br />SvelteKit app
	</h1>

	<h2>
		try editing <strong>src/routes/+page.svelte</strong>
	</h2>

	<div>Hello world</div>
	<div>This is where I will display music information, and hopefully play a song</div>
	<div>song name</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
