import { type SubmitEvent, useState } from "react";
import "./App.css";

function App() {
	const [result, setResult] = useState("");

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
			</section>

			<div className="ticks"></div>
			<section id="spacer"></section>
		</>
	);
}

export default App;
