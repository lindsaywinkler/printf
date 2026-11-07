import { type SubmitEvent, useEffect, useState } from "react";
import "./App.css";

type Part = {
	id: number;
	name: string;
	requiredResolution: number;
	requiredMaterial: { name: string } | null;
	dueTime: string;
	height: number;
	volume: number;
	buildId: number | null;
};

const PARTS_QUERY = `{
	parts {
		id
		name
		requiredResolution
		requiredMaterial {
			name
		}
		dueTime
		height
		volume
		buildId
	}
}`;

async function fetchUpcomingParts(): Promise<Part[]> {
	const response = await fetch("/graphql", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ query: PARTS_QUERY }),
	});
	const { data } = await response.json();
	const now = new Date();
	return data.parts.filter((part: Part) => new Date(part.dueTime) > now);
}

function App() {
	const [result, setResult] = useState("");
	const [parts, setParts] = useState<Part[]>([]);

	useEffect(() => {
		fetchUpcomingParts()
			.then(setParts)
			.catch((error) => setResult(String(error)));
	}, []);

	async function submitPart(event: SubmitEvent<HTMLFormElement>) {
		event.preventDefault();
		const form = new FormData(event.currentTarget);

		try {
			const response = await fetch("/parts", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					name: form.get("name"),
					required_resolution: Number(form.get("required_resolution")),
					required_material_id: Number(form.get("required_material_id")),
					due_time: new Date(form.get("due_time") as string).toISOString(),
					height: Number(form.get("height")),
					volume: Number(form.get("volume")),
				}),
			});
			setResult(`${response.status}: ${await response.text()}`);
			setParts(await fetchUpcomingParts());
		} catch (error) {
			setResult(String(error));
		}
	}

	return (
		<>
			<section id="center">
				<div>
					<h1>printf :-)</h1>
					<p>
						A sketch of a very simple print farm manager, for 3D resin printers.
					</p>
				</div>

				<div>Submit a part for printing:</div>

				<form className="part-form" onSubmit={submitPart}>
					<label>
						Name
						<input name="name" />
					</label>
					<label>
						Resolution (microns)
						<input name="required_resolution" type="number" />
					</label>
					<label>
						Material ID
						<input name="required_material_id" type="number" />
					</label>
					<label>
						Due time
						<input name="due_time" type="datetime-local" />
					</label>
					<label>
						Height (mm)
						<input name="height" type="number" step="any" />
					</label>
					<label>
						Volume (cm³)
						<input name="volume" type="number" step="any" />
					</label>
					<button type="submit">Submit part</button>
				</form>

				{result && <pre>{result}</pre>}

				<div>Upcoming parts:</div>

				<ul className="part-list">
					{parts.map((part) => (
						<li key={part.id}>
							#{part.id} {part.name} · {part.requiredResolution} microns ·{" "}
							{part.requiredMaterial?.name ?? "no material"} · due{" "}
							{new Date(part.dueTime).toLocaleString()} · {part.height} mm ·{" "}
							{part.volume} cm³ ·{" "}
							{part.buildId === null ? "no build" : `build ${part.buildId}`}
						</li>
					))}
				</ul>
			</section>

			<div className="ticks"></div>
			<section id="spacer"></section>
		</>
	);
}

export default App;
