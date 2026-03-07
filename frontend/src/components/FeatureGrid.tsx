import { Zap, Network, UserCheck } from "lucide-react";

const features = [
    {
        name: "Groq Audio Transcription",
        description: "Blisteringly fast OGG voice-to-text processing using the whisper-large-v3 model. Don't leave your customers waiting for a response.",
        icon: Zap,
    },
    {
        name: "LangGraph Intent Routing",
        description: "Intelligent state machine architecture. Classifies text into strict paths like ORDER_STATUS or REFUND_REQUEST, instantly querying your database.",
        icon: Network,
    },
    {
        name: "Zendesk Human Handoff",
        description: "Enterprise-grade fallback. When the AI hits a wall or senses frustration, it smoothly hands over the context to a live support ticket.",
        icon: UserCheck,
    },
];

export function FeatureGrid() {
    return (
        <div id="features" className="bg-white py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl lg:text-center">
                    <h2 className="text-base font-semibold leading-7 text-indigo-600">Enterprise AI</h2>
                    <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                        Everything you need for autonomous support
                    </p>
                    <p className="mt-6 text-lg leading-8 text-gray-600">
                        Engineered specifically for the Indian market, handling Hinglish and mixed-media inputs with perfect reliability.
                    </p>
                </div>

                <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
                    <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-3 lg:gap-y-16">
                        {features.map((feature) => (
                            <div key={feature.name} className="relative pl-16">
                                <dt className="text-base font-semibold leading-7 text-gray-900">
                                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                                        <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                                    </div>
                                    {feature.name}
                                </dt>
                                <dd className="mt-2 text-base leading-7 text-gray-600">{feature.description}</dd>
                            </div>
                        ))}
                    </dl>
                </div>
            </div>
        </div>
    );
}
