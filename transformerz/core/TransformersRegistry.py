import typing


class PathSearch:
	__slots__ = ("registry", "incrFloydWarshal")

	def __init__(self) -> None:
		self.registry = {}
		self.incrFloydWarshal = {}

	def getPath(self, src, tgt):
		if src not in self.registry:
			return ()
		tgtSet = self.registry[src]
		if tgt in tgtSet:
			return (tgtSet[tgt],)

		if tgt in self.incrFloydWarshal:
			tmp = self.incrFloydWarshal[src]
		else:
			self.incrFloydWarshal[src] = tmp = {}

		print("tmp init:", tmp)

		vertexesToObserve = [src]
		currentPath = []
		currentLength = 0

		found = 0
		while vertexesToObserve:
			frontier = []
			for currentVertex in vertexesToObserve:
				if currentVertex not in tmp:
					tmp[currentVertex] = currentLength
				if currentVertex == tgt:
					break
				print("currentVertex", currentVertex, "tgt", tgt)
				if currentVertex in self.registry:
					for nextV in self.registry[currentVertex].keys():
						frontier.append(nextV)
			currentLength = currentLength + 1  # 1 is edge weight
			vertexesToObserve = frontier

		path = []
		curFmt = tgt
		for curPathLen in reversed(range(tmp[tgt])):
			for fi, pl in tmp.items():
				if pl == curPathLen:
					path.append(self.registry[fi][curFmt])
					curFmt = fi
					break
		path.reverse()
		return path

	def addEdge(self, src: typing.Union[typing.Type[str], typing.Type[bytes]], tgt: typing.Iterable[type], obj: typing.Optional["TransformerBase"] = None) -> None:
		if src in self.registry:
			subDic = self.registry[src]
		else:
			self.registry[src] = subDic = {}

		subDic[tgt] = obj


class TransformersRegistry(PathSearch):
	__slots__ = ("mapping",)

	def __init__(self) -> None:
		super().__init__()
		self.mapping = {}

	def getPath(self, src, tgt):
		return super().getPath(src, tgt)

	def __contains__(self, k):
		return k in self.mapping

	def __getitem__(self, k):
		return self.mapping[k]

	def register(self, transformer: typing.Type["TransformerBase"]) -> None:
		tgtType = transformer.tgtType
		srcType = transformer.srcType
		#print("transformer", transformer, "srcType", srcType, "tgtType", tgtType)

		if tgtType is None or srcType is None or srcType is tgtType:
			return
		self.mapping[transformer.id] = transformer
		self.addEdge(srcType, tgtType, transformer)


registry = TransformersRegistry()
