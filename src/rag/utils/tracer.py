from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor,ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

#set provider
provider=TracerProvider()
trace.set_tracer_provider(provider)

#exporter
processor=BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

provider = TracerProvider(
    resource=Resource.create({"service.name": "rag-system"})
)

#tracer object
tracer=trace.get_tracer("rag_tracer")