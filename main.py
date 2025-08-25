from bs4 import BeautifulSoup


def analyzeSVG(svgFile):
    """
    Analyze and print the complete structure of an SVG file.

    Args:
        svgFile (str): Path to the SVG file
    """
    shapesList = ['rect', 'circle', 'ellipse',
                  'line', 'polyline', 'polygon', 'path']
    keyAttrs = ['x', 'y', 'width', 'height', 'cx',
                'cy', 'r', 'rx', 'ry', 'd', 'points']

    with open(svgFile, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'xml')

    print("="*80)
    print(f"SVG STRUCTURE ANALYSIS: {svgFile}")
    print("="*80)

    # 1. Root SVG element info
    svgElms = soup.find('svg')
    if svgElms:
        print("\n🎨 ROOT SVG ELEMENT:")
        print("-" * 40)
        for attr, value in svgElms.attrs.items():
            print(f"  {attr}: {value}")

    # 2. All element types in the SVG
    allElms = soup.find_all()
    elmCounts = {}
    for elm in allElms:
        elmCounts[elm.name] = elmCounts.get(elm.name, 0) + 1

    print(f"\n📊 ELEMENT SUMMARY:")
    print("-" * 40)
    for elmType, count in sorted(elmCounts.items()):
        print(f"  {elmType}: {count}")

    # 3. Text elements analysis
    txtElms = soup.find_all(['text', 'tspan'])
    if txtElms:
        print(f"\n📝 TEXT ELEMENTS ({len(txtElms)} found):")
        print("-" * 40)
        for i, elm in enumerate(txtElms):
            txtContent = elm.get_text(strip=True)
            if txtContent:  # Only show elements with actual text
                print(f"  [{i}] <{elm.name}>")
                print(f"      Text: '{txtContent}'")
                print(f"      Attributes: {dict(elm.attrs)}\n")

    # 4. Groups and layers
    groups = soup.find_all('g')
    if groups:
        print(f"\n🗂️  GROUPS/LAYERS ({len(groups)} found):")
        print("-" * 40)
        for i, group in enumerate(groups):
            print(f"  [{i}] <g>")
            attrs = dict(group.attrs)
            if attrs:
                print(f"      Attributes: {attrs}")

            # Count children
            children = group.find_all(recursive=False)
            childTypes = {}
            for child in children:
                childTypes[child.name] = childTypes.get(child.name, 0) + 1

            if childTypes:
                print(f"      Children: {dict(childTypes)}\n")

    # 5. Shape elements
    shapes = soup.find_all(shapesList)
    if shapes:
        print(f"\n🔷 SHAPE ELEMENTS ({len(shapes)} found):")
        print("-" * 40)
        for i, shape in enumerate(shapes):
            print(f"  [{i}] <{shape.name}>")
            attrs = dict(shape.attrs)
            # Show key positioning/sizing attributes
            relevantAttrs = {k: v for k, v in attrs.items() if k in keyAttrs}
            if relevantAttrs:
                print(f"      Geometry: {relevantAttrs}")

            # Show styling
            style_attrs = {k: v for k, v in attrs.items(
            ) if k in ['fill', 'stroke', 'style', 'class']}
            if style_attrs:
                print(f"      Style: {style_attrs}\n")

    # 6. Images
    images = soup.find_all('image')
    if images:
        print(f"\n🖼️  IMAGES ({len(images)} found):")
        print("-" * 40)
        for i, img in enumerate(images):
            print(f"  [{i}] <image>")
            attrs = dict(img.attrs)
            print(f"      Attributes: {attrs}\n")

    # 7. Definitions (defs) - gradients, patterns, etc.
    defs = soup.find_all('defs')
    if defs:
        print(f"\n🔧 DEFINITIONS ({len(defs)} found):")
        print("-" * 40)
        for i, defElm in enumerate(defs):
            print(f"  [{i}] <defs>")
            children = defElm.find_all(recursive=False)
            for j, child in enumerate(children):
                print(f"      [{j}] <{child.name}> {dict(child.attrs)}\n")


def svgHierarchy(svgFile, maxDepth=3):
    """
    Print the hierarchical structure of the SVG.

    Args:
        svgFile (str): Path to the SVG file
        maxDepth (int): Maximum depth to traverse
    """
    with open(svgFile, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'xml')

    print("\n" + "="*80)
    print("🌳 SVG HIERARCHY TREE")
    print("="*80)

    def elmStructure(elm, depth=0, maxDepth=maxDepth):
        if depth > maxDepth:
            return

        indent = "  " * depth

        # Element info
        tagInfo = f"<{elm.name}>"

        # Add key attributes
        keyAttrs = []
        if elm.get('id'):
            keyAttrs.append(f"id='{elm.get('id')}'")
        if elm.get('class'):
            keyAttrs.append(f"class='{elm.get('class')}'")
        if elm.name in ['text', 'tspan'] and elm.get_text(strip=True):
            text = elm.get_text(strip=True)[
                :30] + "..." if len(elm.get_text(strip=True)) > 30 else elm.get_text(strip=True)
            keyAttrs.append(f"text='{text}'")

        if keyAttrs:
            tagInfo += f" [{', '.join(keyAttrs)}]"

        print(f"{indent}{tagInfo}")

        # Process children
        children = elm.find_all(recursive=False)
        for child in children:
            elmStructure(child, depth + 1, maxDepth)

    svgRoot = soup.find('svg')
    if svgRoot:
        elmStructure(svgRoot)


def extractTxtElm(svgFile):
    """
    Extract detailed information about all text elements.

    Args:
        svgFile (str): Path to the SVG file
    """
    with open(svgFile, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'xml')

    print("\n" + "="*80)
    print("📝 DETAILED TEXT ANALYSIS")
    print("="*80)

    txtElms = soup.find_all(['text', 'tspan'])

    for i, elm in enumerate(txtElms):
        txtContent = elm.get_text(strip=True)
        if txtContent:
            print(f"\n[{i}] TEXT ELEMENT:")
            print(f"    Tag: <{elm.name}>")
            print(f"    Content: '{txtContent}'")
            print(f"    Length: {len(txtContent)} characters")

            # Position
            x = elm.get('x', 'N/A')
            y = elm.get('y', 'N/A')
            print(f"    Position: x={x}, y={y}")

            # Styling
            styleAttrs = {}
            for attr in ['font-family', 'font-size', 'font-weight', 'fill', 'stroke', 'style']:
                if elm.get(attr):
                    styleAttrs[attr] = elm.get(attr)

            if styleAttrs:
                print(f"    Styling: {styleAttrs}")

            # Parent info
            parent = elm.parent
            if parent and parent.name != 'svg':
                print(
                    f"    Parent: <{parent.name}> {dict(parent.attrs) if parent.attrs else ''}")

            print("-" * 50)


if __name__ == '__main__':
    svgFile = 'little_tower.svg'
    analyzeSVG(svgFile)
    svgHierarchy(svgFile)
    extractTxtElm(svgFile)
