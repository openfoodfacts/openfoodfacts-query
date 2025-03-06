from query.db import Database
from query.models.query import Filter, GroupStage, Stage
from query.services import query
from query.services.query_count_test import create_test_tags


async def test_group_products_with_a_tag():
    async with Database() as connection:
        tags = await create_test_tags(connection)
        response = await query.aggregate([Stage(match=Filter(), group=GroupStage(id='$origins_tags'))])
        my_result = [result for result in response if result.id == tags.origin_value]
        assert len(my_result) == 1
        assert my_result[0].count == 3


#   it('should filter products when grouping', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value, amino_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.aggregate([
#         { $match: { amino_acids_tags: amino_value } },
#         { $group: { _id: '$origins_tags' } },
#       ]);
#       const my_tag = response.find((r) => r._id === origin_value);
#       expect(my_tag).to_be_truthy();
#       expect(parse_int(my_tag.count)).to_be(2);
#     });
#   });

#   it('should filter products when grouping by a product field', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { amino_value, creator_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.aggregate([
#         { $match: { amino_acids_tags: amino_value } },
#         { $group: { _id: '$creator' } },
#       ]);
#       const my_tag = response.find((r) => r._id === creator_value);
#       expect(my_tag).to_be_truthy();
#       expect(parse_int(my_tag.count)).to_be(1);
#     });
#   });

#   it('should group products when filtering by a product field', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { amino_value, creator_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.aggregate([
#         { $match: { creator: creator_value } },
#         { $group: { _id: '$amino_acids_tags' } },
#       ]);
#       const my_tag = response.find((r) => r._id === amino_value);
#       expect(my_tag).to_be_truthy();
#       expect(parse_int(my_tag.count)).to_be(1);
#     });
#   });

#   it('should be able to do not filtering', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value, amino_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.aggregate([
#         { $match: { amino_acids_tags: { $ne: amino_value } } },
#         { $group: { _id: '$origins_tags' } },
#       ]);
#       const my_tag = response.find((r) => r._id === origin_value);
#       expect(my_tag).to_be_truthy();
#       expect(parse_int(my_tag.count)).to_be(1);
#     });
#   });

#   it('should be able to just count', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const query_service = app.get(query_service);
#       const query: aggregate_query = [
#         { $match: {} },
#         { $group: { _id: '$origins_tags' } },
#         { $count: 1 },
#       ];
#       const before_response = await query_service.aggregate(query);
#       const before_count = parse_int(before_response['origins_tags']);

#       await create_test_tags(app);
#       const response = await query_service.aggregate(query);
#       expect(parse_int(response['origins_tags'])).to_be(before_count + 1);
#     });
#   });

#   it('should cope with multiple filters', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value, amino_value, neucleotide_value } =
#         await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.aggregate([
#         {
#           $match: {
#             amino_acids_tags: amino_value,
#             nucleotides_tags: neucleotide_value,
#           },
#         },
#         { $group: { _id: '$origins_tags' } },
#       ]);
#       const my_tag = response.find((r) => r._id === origin_value);
#       expect(my_tag).to_be_truthy();
#       expect(parse_int(my_tag.count)).to_be(1);
#     });
#   });

#   it('should be able to group obsolete products', async () => {
#     await create_testing_module([domain_module], async (app) => {
#       const { origin_value } = await create_test_tags(app);
#       const query_service = app.get(query_service);
#       const response = await query_service.aggregate(
#         [{ $match: {} }, { $group: { _id: '$origins_tags' } }],
#         true,
#       );
#       const my_tag = response.find((r) => r._id === origin_value);
#       expect(my_tag).to_be_truthy();
#       expect(parse_int(my_tag.count)).to_be(1);
#     });
#   });
# });
