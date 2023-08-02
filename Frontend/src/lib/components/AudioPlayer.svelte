<script context="module">
	let current;
</script>

<script>
	export let src;
	export let title;
	export let artist;
	export let album;

	let audio;
	let paused = true;

	function stopOthers() {
		if (current && current !== audio) current.pause();
		current = audio;
	}
</script>

<article class="w-full" class:playing={!paused}>
	<h2>{title}</h2>
	<p class="whitespace-nowrap"><strong>{artist}</strong> / album name: {album}</p>
	<audio class="w-full h-10" bind:this={audio} bind:paused on:play={stopOthers} controls {src} />
</article>

<style>
	article {
		max-width: 800px;
	}

	.playing {
		color: #da0303;
	}
</style>
