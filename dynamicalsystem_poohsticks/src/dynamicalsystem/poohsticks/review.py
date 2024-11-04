from dynamicalsystem.poohsticks.notion import Notion


class Review:
    def __init__(self, chart, placing) -> None:
        self.chart = chart
        self.placing = placing
        self.publishers = []
        self.notion = Notion(chart, placing)


"""
	def publish(self):
		watermarks = Watermarks()

		publish = []
		missing = []
		for k, v in watermarks.watermarks.items():
			try:
				r = Review(chart='tQ24.5', placing=v)
			except ValueError as e:  # no review found
				logger.exception((f'{str(e)} Publisher {k}.'))
				continue

			if d := r.notion.validate_content():
				d['chart'] = r.notion.chart
				d['placing'] = r.notion.placing
				d['publisher'] = k
				d['message'] = (
					f"{r.notion.chart}.{r.notion.placing}\n"
					f"{possessive(d['artist'])} \"{d['work']}\"\n"
					f"{d['review']}\n{d['verdict']}"
				)

				publish.append(d)
			else:
				missing.append(r.notion.content)
		
		for d in publish:
			publisher = None
			if d['publisher'] == 'signal_messenger':
				publisher = SignalMessenger(message=d['message'])
			elif d['publisher'] == 'bluesky':
				publisher = BlueSky(message=d['message'])
			elif d['publisher'] == 'tester':
				publisher = Validator(message=d['message'])

			if publisher:
				if publisher.publish():
					logger.info(f'{d["publisher"]}')
					watermarks.update_watermark(d['publisher'])
				else:
					logger.error(f'Publish failed for {d.get("publisher")}, chart {d.get("chart")}, placing {d.get("placing")}.')


		for s in missing:
			logger.warning('Failed to publish\n{s}\n')
"""
