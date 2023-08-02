<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import { PUBLIC_CLIENT_ID, PUBLIC_CLIENT_SECRET } from '$env/static/public';
	import AudioPlayer from '$lib/components/AudioPlayer.svelte';
	import { onMount } from 'svelte';
	let songs = [];
	async function get_token() {
		let auth_string = PUBLIC_CLIENT_ID + ':' + PUBLIC_CLIENT_SECRET;
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
			return res1['access_token'];
		} else {
			console.log("get token didn't work");
			return null;
		}
	}

	async function search_for_artist(auth_header, artist_name) {
		let url = 'https://api.spotify.com/v1/search';
		let headers = auth_header;
		let query = `?q=${artist_name}&type=artist&limit=2`;
		let query_url = url + query;
		const response = await fetch(query_url, {
			method: 'GET',
			headers: headers
		});
		if (response.ok) {
			let res2 = await response.json();
			return {
				artist_name: res2.artists.items[0].name,
				artist_id: res2.artists.items[0].id
			};
		} else {
			console.log("the search for artist call didn't work");
			return null;
		}
	}

	async function get_songs_by_artist(auth_header, artist_id) {
		const url = `https://api.spotify.com/v1/artists/${artist_id}/top-tracks?country=US`;
		const headers = auth_header;
		// result = get(url, headers=headers)
		const result = await fetch(url, {
			method: 'GET',
			headers: headers
		});
		const res3 = await result.json();
		// console.log(res3);
		return res3.tracks;
	}

	onMount(async () => {
		// console.log(PUBLIC_CLIENT_ID);
		// console.log(PUBLIC_CLIENT_SECRET);
		let token = await get_token();
		// console.log(token);
		const auth_header = { Authorization: 'Bearer ' + token };
		// console.log({ auth_header });
		let artist_res = await search_for_artist(auth_header, 'ACDC');
		console.log(artist_res);

		songs = await get_songs_by_artist(auth_header, artist_res.artist_id);
		console.log(songs);
		//try to grab a list of songs to generally display such as top tracks or playlists?
		//refer to main.py to convert get call into a fetch to be used in onmount
		//create a stores value for your consistently used access token

		// try to grab a song too?
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
	</h1>

	<div class="text-lg text-black font-bold">song names (top ten)</div>
	<div class="flex flex-col justify-start gap-4">
		{#each songs as song, i}
			<div class="flex flex-row w-full bg-gray-400 items-start gap-2 rounded-xl px-4 py-2">
				<div>{i + 1}.</div>
				<div>
					<img
						class="min-w-[100px] h-[100px] aspect-square object-cover rounded-lg"
						src={song.album.images[0].url}
						alt=""
					/>
				</div>

				<AudioPlayer
					src={song.preview_url}
					title={song.name}
					album={song.album.name}
					artist={song.artists[0].name}
				/>

				<!-- <iframe
					style="border-radius:12px"
					src={`https://open.spotify.com/embed/track/${song.id}?utm_source=generator`}
					width="100%"
					height="100"
					frameBorder="0"
					allowfullscreen=""
					allow="encrypted-media"
					loading="lazy"
					title=""
				/> -->

				<!-- <iframe
					title="Current Song"
					allow="encrypted-media"
					src={`https://open.spotify.com/embed/track/${song.uri}?utm_source=oembed`}
				/> -->
			</div>
		{/each}
	</div>
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
