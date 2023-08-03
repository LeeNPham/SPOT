<script>
	import AudioPlayer from '$lib/components/AudioPlayer.svelte';
	import { auth_header } from '$store/stores';

	let songs = [];
	let artist_name = '';
	let artist_res;
	let artist_id;

	async function search_for_artist(artist_name) {
		let url = 'https://api.spotify.com/v1/search';
		let query = `?q=${artist_name}&type=artist&limit=2`;
		let query_url = url + query;
		const response = await fetch(query_url, {
			method: 'GET',
			headers: $auth_header
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

	async function get_songs_by_artist(artist_id) {
		const url = `https://api.spotify.com/v1/artists/${artist_id}/top-tracks?country=US`;
		const result = await fetch(url, {
			method: 'GET',
			headers: $auth_header
		});
		const res3 = await result.json();
		return res3.tracks;
	}
</script>

<svelte:head>
	<title>Search</title>
	<meta name="description" content="Search by Artist page" />
</svelte:head>

<section>
	<div class="text-lg text-black font-bold">Search for Artist:</div>
	<div class="flex flex-col gap-4">
		<form class="flex gap-4 items-center flex-row" on:submit={() => search_for_artist(artist_name)}>
			<input
				required
				type="text"
				bind:value={artist_name}
				class="p-2 border rounded-full w-full border-gray-200 h-7 focus:ring-0"
			/>
			<button
				type="submit"
				class="px-2 py-1 bg-blue-500 hover:bg-blue-500/90 text-white rounded-full h-7 flex items-center text-sm"
			>
				Search
			</button>
		</form>
	</div>
	<div class="text-lg text-black font-bold">song names (top ten)</div>
	<div class="flex flex-col justify-start gap-4">
		{#if artist_id != undefined}
			{#await get_songs_by_artist(artist_id)}
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
