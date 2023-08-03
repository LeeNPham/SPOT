<script>
	import { PUBLIC_CLIENT_ID, PUBLIC_CLIENT_SECRET } from '$env/static/public';
	import AudioPlayer from '$lib/components/AudioPlayer.svelte';
	import { onMount } from 'svelte';
	let songs = [];
	let artist_name = '';
	let auth_header = '';
	let artist_res;
	let token;
	let artist_id;

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
			artist_id = res2.artists.items[0].id;
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

		const result = await fetch(url, {
			method: 'GET',
			headers: headers
		});
		const res3 = await result.json();
		return res3.tracks;
	}

	onMount(async () => {
		token = await get_token();
		auth_header = { Authorization: 'Bearer ' + token };
	});
</script>

<svelte:head>
	<title>Search</title>
	<meta name="description" content="Search by Artist page" />
</svelte:head>

<section>
	<div class="text-lg text-black font-bold">Search for Artist:</div>
	<div class="flex flex-col gap-4">
		<input
			type="text"
			bind:value={artist_name}
			class="p-2 border rounded-full w-full border-gray-200 h-7"
		/>
		<button
			on:click={() => search_for_artist(auth_header, artist_name)}
			class="px-4 py-2 bg-blue-500 text-white rounded"
		>
			Search
		</button>
	</div>
	<div class="text-lg text-black font-bold">song names (top ten)</div>
	<div class="flex flex-col justify-start gap-4">
		{#if artist_id != undefined}
			{#await get_songs_by_artist(auth_header, artist_id)}
				Please provide an artist name for us to provide you their top ten tracks
			{:then songs}
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
					</div>
				{/each}
			{:catch error}
				{error}
			{/await}
		{/if}
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
</style>
