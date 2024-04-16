import { client } from "@gradio/client";

const app = await client("https://b05029ad640abbade7.gradio.live/");
const result = await app.predict("/chat", [		
				"Hello!!", // string  in 'Message' Textbox component
	]);

console.log(result.data);
